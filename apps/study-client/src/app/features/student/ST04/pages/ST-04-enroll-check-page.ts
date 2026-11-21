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
  private courseId: string | null = null;

  ngOnInit(): void {
    const courseId = this.route.snapshot.paramMap.get('courseId');
    if (!courseId) {
      this.loadState.set('missing');
      return;
    }
    this.courseId = courseId;
    this.api
      .getCourse(courseId)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (course) => {
          this.course.set(course);
          if (!course) return this.loadState.set('error');
          this.loadState.set('checking');
          this.api.getProgress(courseId).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
            next: (response) => this.loadState.set(response.success ? 'enrolled' : 'error'),
            error: (error: unknown) => {
              if (error instanceof HttpErrorResponse && error.status === 404) {
                const price = Number(course.price);
                this.loadState.set(Number.isFinite(price) && price >= 0 ? (price === 0 ? 'free' : 'paid') : 'error');
              } else {
                this.loadState.set('error');
              }
            },
          });
        },
        error: (error: unknown) =>
          this.loadState.set(
            error instanceof HttpErrorResponse && error.status === 404 ? 'missing' : 'error',
          ),
      });
  }

  enroll(): void {
    if (this.loadState() !== 'free' || !this.courseId) return;
    this.loadState.set('enrolling');
    this.api.enroll(this.courseId).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (response) => this.loadState.set(response.success && response.data?.status === 'ACTIVE' ? 'enrolled' : 'error'),
      error: () => this.loadState.set('error'),
    });
  }
}
