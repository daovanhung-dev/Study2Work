import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DestroyRef } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { St05CourseApi } from '../data-access/ST-05-checkout-course.service';
import {
  type St05CourseLoadState,
  type St05CourseSummary,
} from '../models/ST-05-checkout-course.models';
import { StudentOrderCheckView } from '../ui/ST-05-order-check-view';

@Component({
  selector: 'study-student-order-check-page',
  imports: [StudentOrderCheckView],
  templateUrl: './ST-05-order-check-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentOrderCheckPage implements OnInit {
  private readonly destroyRef = inject(DestroyRef);
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(St05CourseApi);
  readonly course = signal<St05CourseSummary | null>(null);
  readonly loadState = signal<St05CourseLoadState>('loading');
  backToEnrollUrl = '/student';

  ngOnInit(): void {
    const courseId = this.route.snapshot.paramMap.get('courseId');
    if (!courseId) {
      this.loadState.set('missing');
      return;
    }
    this.backToEnrollUrl = `/student/enroll/${encodeURIComponent(courseId)}`;
    this.api
      .getCourse(courseId)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (course) => {
          this.course.set(course);
          this.loadState.set(course ? 'ready' : 'error');
        },
        error: (error: unknown) =>
          this.loadState.set(
            error instanceof HttpErrorResponse && error.status === 404 ? 'missing' : 'error',
          ),
      });
  }
}
