import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink, RouterLinkActive } from '@angular/router';
import { catchError, distinctUntilChanged, map, of, switchMap } from 'rxjs';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { GuestPublicCoursePage } from '../../../guest/shared/models/guest-course.models';
import { GS03CourseDetailService } from '../../../guest/GS03/data-access/gs03-course-detail.service';

type EnrollmentGateState = 'loading' | 'gate' | 'not-found' | 'error';

@Component({
  imports: [RouterLink, RouterLinkActive],
  selector: 'study-st04-page',
  templateUrl: './st04-page.html',
})
export class ST04Page {
  private readonly route = inject(ActivatedRoute);
  private readonly destroyRef = inject(DestroyRef);
  private readonly courseDetail = inject(GS03CourseDetailService);

  readonly state = signal<EnrollmentGateState>('loading');

  constructor() {
    this.route.paramMap
      .pipe(
        map((params) => params.get('courseId') ?? ''),
        distinctUntilChanged(),
        switchMap((courseId) => {
          if (!courseId) return of<EnrollmentGateState>('not-found');

          this.state.set('loading');
          return this.courseDetail.getCourse(courseId).pipe(
            map((response) => this.mapCourseResponse(response)),
            catchError((error: unknown) => of(this.mapCourseError(error))),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((state) => this.state.set(state));
  }

  private mapCourseResponse(response: ApiEnvelope<GuestPublicCoursePage>): EnrollmentGateState {
    if (!response.success || response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') return 'error';

    const course = response.data.items[0];
    return course?.status === 'PUBLISHED' ? 'gate' : 'not-found';
  }

  private mapCourseError(error: unknown): EnrollmentGateState {
    return error instanceof HttpErrorResponse && error.status === 404 ? 'not-found' : 'error';
  }
}
