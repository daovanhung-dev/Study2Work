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

const MAX_COURSE_ID = 9_223_372_036_854_775_807n;

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
  backLabel = 'Về trang học viên';

  ngOnInit(): void {
    const courseId = this.route.snapshot.paramMap.get('courseId');
    if (!isValidCourseId(courseId)) {
      this.loadState.set('missing');
      return;
    }
    this.backToEnrollUrl = '/student/enroll/' + courseId;
    this.backLabel = 'Quay lại kiểm tra ghi danh';
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

function isValidCourseId(value: string | null): value is string {
  return value !== null && /^[1-9]\d*$/.test(value) && BigInt(value) <= MAX_COURSE_ID;
}
