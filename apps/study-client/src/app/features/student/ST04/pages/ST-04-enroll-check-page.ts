import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DestroyRef } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { St04CourseApi } from '../data-access/ST-04-enroll-course.service';
import {
  type St04CourseLoadState,
  type St04CourseSummary,
} from '../models/ST-04-enroll-course.models';
import { StudentEnrollCheckView } from '../ui/ST-04-enroll-check-view';

@Component({
  selector: 'study-student-enroll-check-page',
  imports: [StudentEnrollCheckView],
  templateUrl: './ST-04-enroll-check-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentEnrollCheckPage implements OnInit {
  private readonly destroyRef = inject(DestroyRef);
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(St04CourseApi);
  readonly course = signal<St04CourseSummary | null>(null);
  readonly loadState = signal<St04CourseLoadState>('loading');

  ngOnInit(): void {
    const courseId = this.route.snapshot.paramMap.get('courseId');
    if (!courseId) {
      this.loadState.set('missing');
      return;
    }
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
