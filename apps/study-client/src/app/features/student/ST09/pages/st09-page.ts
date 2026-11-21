import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { ActivatedRoute, RouterLink } from '@angular/router';
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
import type { Observable } from 'rxjs';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { ST09CourseOverviewService } from '../data-access/st09-course-overview.service';
import {
  hasStudentCoursePageCountMismatch,
  isStudentCoursePage,
} from '../../shared/models/student-course-page.guard';
import { isStudentCourseProgress } from '../../shared/models/student-course-progress.guard';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type {
  StudentCourseProgress,
  StudentCourseSummary,
} from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';
import { StudentPublicFrame } from '../../../../shared/ui/student-public-frame';

@Component({
  imports: [RouterLink, StudentPublicFrame],
  selector: 'study-st09-page',
  styleUrls: ['./st09-page.css', '../../shared/ui/student-api-page.css'],
  templateUrl: './st09-page.html',
})
export class ST09Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST09CourseOverviewService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly retryOverview$ = new Subject<void>();
  readonly courseId = signal(toSafeStudyId(this.route.snapshot.paramMap.get('courseId')));
  readonly enrollmentLoading = signal(true);
  readonly progressLoading = signal(false);
  readonly error = signal<string | null>(null);
  readonly course = signal<StudentCourseSummary | null>(null);
  readonly progress = signal<StudentCourseProgress | null>(null);
  readonly notEnrolled = signal(false);
  readonly snapshotMismatch = signal(false);

  ngOnInit(): void {
    const courseId$ = this.route.paramMap.pipe(
      map((params) => toSafeStudyId(params.get('courseId'))),
      distinctUntilChanged(),
      tap((courseId) => this.courseId.set(courseId)),
    );

    combineLatest([courseId$, this.retryOverview$.pipe(startWith(undefined))])
      .pipe(
        tap(() => {
          this.enrollmentLoading.set(true);
          this.progressLoading.set(false);
          this.error.set(null);
          this.course.set(null);
          this.progress.set(null);
          this.notEnrolled.set(false);
          this.snapshotMismatch.set(false);
        }),
        switchMap(([courseId]) => this.loadOverview(courseId)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyOverviewResult(result));
  }

  retry(): void {
    if (this.courseId()) this.retryOverview$.next();
  }

  progressWidth(): number {
    return Math.max(0, Math.min(100, this.progress()?.progress_percent ?? 0));
  }

  private loadOverview(courseId: string | null): Observable<OverviewResult> {
    if (!courseId) return of({ type: 'invalid-course-id' });

    return this.findActiveCourse(courseId, 1).pipe(
      switchMap((lookup) => {
        if (lookup.type !== 'found') return of(lookup);

        this.course.set(lookup.course);
        this.snapshotMismatch.set(lookup.snapshotMismatch);
        this.enrollmentLoading.set(false);
        this.progressLoading.set(true);
        return this.data.progress(courseId).pipe(
          map((response) => ({ type: 'progress', courseId, response }) as const),
          catchError((error: unknown) => of({ type: 'progress-error', error } as const)),
        );
      }),
      catchError((error: unknown) =>
        of({ type: 'request-error', message: studentApiErrorMessage(error) } as const),
      ),
    );
  }

  private findActiveCourse(courseId: string, page: number): Observable<CourseLookupResult> {
    return this.data.activeCourses(page).pipe(
      switchMap((response) => {
        const issue = envelopeIssue(response);
        if (issue) return of({ type: 'request-error', message: issue } as const);
        if (response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
          return of({
            type: 'request-error',
            message: 'Chưa thể xác nhận khóa học đang hoạt động.',
          } as const);
        }
        if (!isStudentCoursePage(response.data, page, 'ACTIVE')) {
          return of({
            type: 'request-error',
            message: 'Danh sách khóa học chưa đúng định dạng. Hãy tải lại trang.',
          } as const);
        }

        const snapshotMismatch = hasStudentCoursePageCountMismatch(response.data);
        const match = response.data.items.find(
          (item) => toSafeStudyId(item.course_id) === courseId,
        );
        if (match) return of({ type: 'found', course: match, snapshotMismatch } as const);
        if (snapshotMismatch) return of({ type: 'snapshot-mismatch' } as const);
        if (page < response.data.pagination.total_pages) {
          return this.findActiveCourse(courseId, page + 1);
        }
        return of({ type: 'not-enrolled' } as const);
      }),
      catchError((error: unknown) =>
        of({ type: 'request-error', message: studentApiErrorMessage(error) } as const),
      ),
    );
  }

  private applyOverviewResult(result: OverviewResult): void {
    this.progressLoading.set(false);
    if (result.type === 'invalid-course-id') {
      this.error.set('Không tìm thấy khóa học này.');
      this.enrollmentLoading.set(false);
      return;
    }
    if (result.type === 'not-enrolled') {
      this.notEnrolled.set(true);
      this.enrollmentLoading.set(false);
      return;
    }
    if (result.type === 'snapshot-mismatch') {
      this.snapshotMismatch.set(true);
      this.enrollmentLoading.set(false);
      return;
    }
    if (result.type === 'request-error') {
      this.error.set(result.message);
      this.enrollmentLoading.set(false);
      return;
    }
    if (result.type === 'progress-error') {
      if (result.error instanceof HttpErrorResponse && result.error.status === 404) {
        this.error.set('Không còn xác minh được ghi danh hoặc tiến độ cho khóa học này.');
      } else {
        this.error.set(studentApiErrorMessage(result.error));
      }
      return;
    }

    const issue = envelopeIssue(result.response);
    if (issue) {
      this.error.set(issue);
    } else if (result.response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
      this.error.set('Chưa thể tải tiến độ khóa học.');
    } else if (!isStudentCourseProgress(result.response.data, result.courseId)) {
      this.error.set('Dữ liệu tiến độ chưa đúng định dạng. Hãy tải lại trang.');
    } else {
      this.progress.set(result.response.data);
    }
  }
}

type CourseLookupResult =
  | { type: 'found'; course: StudentCourseSummary; snapshotMismatch: boolean }
  | { type: 'snapshot-mismatch' }
  | { type: 'not-enrolled' }
  | { type: 'request-error'; message: string };

type OverviewResult =
  | { type: 'invalid-course-id' }
  | { type: 'snapshot-mismatch' }
  | { type: 'not-enrolled' }
  | { type: 'request-error'; message: string }
  | { type: 'progress'; courseId: string; response: ApiEnvelope<StudentCourseProgress> }
  | { type: 'progress-error'; error: unknown };

function envelopeIssue(value: unknown): string | null {
  if (
    typeof value !== 'object' ||
    value === null ||
    typeof (value as Record<string, unknown>)['success'] !== 'boolean' ||
    typeof (value as Record<string, unknown>)['message'] !== 'string' ||
    typeof (value as Record<string, unknown>)['businessCode'] !== 'string' ||
    !('data' in value)
  ) {
    return 'Yêu cầu chưa được hoàn tất. Vui lòng thử lại.';
  }
  const response = value as ApiEnvelope<unknown>;
  return studentEnvelopeError(response.success, response.message);
}
