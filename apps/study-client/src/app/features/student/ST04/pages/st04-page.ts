import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink, RouterLinkActive } from '@angular/router';
import {
  Subject,
  catchError,
  combineLatest,
  distinctUntilChanged,
  map,
  of,
  startWith,
  switchMap,
  tap,
} from 'rxjs';

import {
  StudentSessionError,
  StudentSessionService,
} from '../../../../core/auth/student-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type {
  GuestPublicCourse,
} from '../../../guest/shared/models/guest-course.models';
import { GS03CourseDetailService } from '../../../guest/GS03/data-access/gs03-course-detail.service';
import type { StudentEnrollment } from '../../shared/models/student-enrollment.models';
import { isStudentEnrollment } from '../../shared/models/student-enrollment.guard';
import {
  hasStudentCoursePageCountMismatch,
  isStudentCoursePage,
} from '../../shared/models/student-course-page.guard';
import { ST04EnrollmentService } from '../data-access/st04-enrollment.service';

type EnrollmentGateState =
  | 'loading'
  | 'not-found'
  | 'error'
  | 'login-required'
  | 'already-enrolled'
  | 'enrollment-unresolved'
  | 'free'
  | 'paid'
  | 'submitting'
  | 'refresh-error';

interface EnrollmentView {
  state: EnrollmentGateState;
  course: GuestPublicCourse | null;
}

@Component({
  imports: [RouterLink, RouterLinkActive],
  selector: 'study-st04-page',
  styleUrl: './st04-page.css',
  templateUrl: './st04-page.html',
})
export class ST04Page {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);
  private readonly courseDetail = inject(GS03CourseDetailService);
  private readonly enrollmentApi = inject(ST04EnrollmentService);
  readonly session = inject(StudentSessionService);
  private readonly retryCheck$ = new Subject<void>();
  private routeGeneration = 0;

  readonly state = signal<EnrollmentGateState>('loading');
  readonly course = signal<GuestPublicCourse | null>(null);

  constructor() {
    const courseId$ = this.route.paramMap
      .pipe(
        map((params) => params.get('courseId') ?? ''),
        distinctUntilChanged(),
        tap(() => (this.routeGeneration += 1)),
      );

    combineLatest([courseId$, this.retryCheck$.pipe(startWith(undefined))])
      .pipe(
        switchMap(([courseId]) => this.loadEnrollmentView(courseId)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe(({ state, course }) => {
        this.course.set(course);
        this.state.set(state);
      });
  }

  retryCheck(): void {
    this.retryCheck$.next();
  }

  goToCheckout(courseId: number): void {
    const safeId = toSafeCourseId(courseId);
    if (safeId === null) return;
    void this.router.navigate(['/student/checkout', String(safeId)]);
  }

  logout(): void {
    this.session.endLocalSession();
  }

  enrollForFree(): void {
    const course = this.course();
    const courseId = course ? toSafeCourseId(course.id) : null;
    if (this.state() !== 'free' || courseId === null) return;

    const routeGeneration = this.routeGeneration;
    this.state.set('submitting');
    this.enrollmentApi
      .enroll(courseId)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          if (routeGeneration !== this.routeGeneration) return;
          if (!response.success || response.businessCode !== 'DESIGN_RESOURCE_CREATED') {
            this.state.set('error');
            return;
          }
          if (!isStudentEnrollment(response.data) || response.data.course_id !== courseId) {
            this.state.set('error');
            return;
          }
          this.refreshMyCourses(courseId, false, routeGeneration);
        },
        error: (error: unknown) => {
          if (routeGeneration !== this.routeGeneration) return;
          if (error instanceof HttpErrorResponse && error.status === 409) {
            this.refreshMyCourses(courseId, true, routeGeneration);
            return;
          }
          this.state.set(mapStudentRequestError(error));
        },
      });
  }

  retryMyCoursesRefresh(): void {
    const course = this.course();
    const courseId = course ? toSafeCourseId(course.id) : null;
    if (courseId !== null && this.state() === 'refresh-error') {
      this.refreshMyCourses(courseId, false, this.routeGeneration);
    }
  }

  private loadEnrollmentView(courseId: string) {
    const safeId = toSafeCourseId(courseId);
    if (safeId === null) return of<EnrollmentView>({ state: 'not-found', course: null });

    this.course.set(null);
    this.state.set('loading');

    return this.courseDetail.getCourse(courseId).pipe(
      switchMap((response) => {
        if (!response.success || response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
          return of<EnrollmentView>({ state: 'error', course: null });
        }
        const course = response.data.items.find((item) => item.id === safeId);
        if (!course || course.status !== 'PUBLISHED') {
          return of<EnrollmentView>({ state: 'not-found', course: null });
        }

        return this.enrollmentApi.enrollmentStatus(courseId).pipe(
          map((enrollment) => this.mapEnrollmentResponse(enrollment, course)),
          catchError((error: unknown) => {
            if (error instanceof HttpErrorResponse && error.status === 404) {
              return of({ state: this.coursePriceState(course), course });
            }
            return of({ state: mapStudentRequestError(error), course });
          }),
        );
      }),
      catchError((error: unknown) =>
        of<EnrollmentView>({
          state: error instanceof HttpErrorResponse && error.status === 404 ? 'not-found' : 'error',
          course: null,
        }),
      ),
    );
  }

  private mapEnrollmentResponse(
    response: ApiEnvelope<StudentEnrollment>,
    course: GuestPublicCourse,
  ): EnrollmentView {
    if (
      !response.success ||
      response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isStudentEnrollment(response.data) ||
      response.data.course_id !== course.id
    ) {
      return { state: 'error', course };
    }
    return {
      state:
        response.data.status.trim().toUpperCase() === 'ACTIVE'
          ? 'already-enrolled'
          : 'enrollment-unresolved',
      course,
    };
  }

  private coursePriceState(course: GuestPublicCourse): EnrollmentGateState {
    const amount = Number(course.price);
    if (!Number.isFinite(amount) || amount < 0) return 'error';
    return amount === 0 ? 'free' : 'paid';
  }

  private refreshMyCourses(courseId: number, conflict: boolean, routeGeneration: number): void {
    this.enrollmentApi
      .courses()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          if (routeGeneration !== this.routeGeneration) return;
          if (
            !response.success ||
            response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
            !isStudentCoursePage(response.data, 1, 'ACTIVE')
          ) {
            this.state.set('refresh-error');
            return;
          }
          const countMismatch = hasStudentCoursePageCountMismatch(response.data);
          if (
            !response.data.items.some(
              (course) => course.course_id === courseId && course.enrollment_status === 'ACTIVE',
            ) ||
            (countMismatch && response.data.items.length === 0)
          ) {
            this.state.set('refresh-error');
            return;
          }
          void this.router.navigateByUrl('/student/courses').then((navigated) => {
            if (routeGeneration !== this.routeGeneration) return;
            if (!navigated) this.state.set('refresh-error');
          });
        },
        error: (error: unknown) => {
          if (routeGeneration !== this.routeGeneration) return;
          this.state.set(conflict ? mapStudentRequestError(error) : 'refresh-error');
        },
      });
  }
}

function mapStudentRequestError(error: unknown): EnrollmentGateState {
  if (error instanceof StudentSessionError && error.code === 'LOGIN_REQUIRED') return 'login-required';
  if (error instanceof HttpErrorResponse && (error.status === 401 || error.status === 403)) {
    return 'login-required';
  }
  return 'error';
}

function toSafeCourseId(value: string | number): number | null {
  if (typeof value === 'string' && !/^[1-9]\d*$/.test(value)) return null;
  const courseId = Number(value);
  return Number.isSafeInteger(courseId) && courseId > 0 ? courseId : null;
}
