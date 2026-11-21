import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
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
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ST21CourseProgressService } from '../data-access/st21-course-progress.service';
import { isStudentCourseProgress } from '../../shared/models/student-course-progress.guard';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import type { StudentCourseProgress } from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [RouterLink],
  selector: 'study-st21-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    '../../shared/ui/student-api-community.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st21-page.html',
})
export class ST21Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST21CourseProgressService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly retryProgress$ = new Subject<void>();
  readonly courseId = signal(toSafeStudyId(this.route.snapshot.paramMap.get('courseId')));
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly progress = signal<StudentCourseProgress | null>(null);

  ngOnInit(): void {
    const courseId$ = this.route.paramMap.pipe(
      map((params) => toSafeStudyId(params.get('courseId'))),
      distinctUntilChanged(),
      tap((courseId) => this.courseId.set(courseId)),
    );
    combineLatest([courseId$, this.retryProgress$.pipe(startWith(undefined))])
      .pipe(
        tap(() => {
          this.loading.set(true);
          this.error.set(null);
          this.progress.set(null);
        }),
        switchMap(([courseId]) => this.loadProgress(courseId)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyProgress(result));
  }

  retryProgress(): void {
    this.retryProgress$.next();
  }

  percentWidth(): number {
    return this.progress()?.progress_percent ?? 0;
  }

  private loadProgress(courseId: string | null) {
    if (!courseId) return of({ courseId, response: null, error: null });
    return this.data.progress(courseId).pipe(
      map((response) => ({ courseId, response, error: null })),
      catchError((error: unknown) => of({ courseId, response: null, error })),
    );
  }

  private applyProgress(result: ProgressLoad): void {
    this.loading.set(false);
    if (!result.courseId) {
      this.error.set('Không tìm thấy khóa học này.');
      return;
    }
    if (result.error !== null) {
      this.error.set(studentApiErrorMessage(result.error));
      return;
    }
    const response = result.response;
    if (!response?.success) {
      this.error.set('Chưa thể tải tiến độ khóa học. Vui lòng thử lại.');
      return;
    }
    if (
      response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isStudentCourseProgress(response.data, result.courseId)
    ) {
      this.error.set('Tiến độ không khớp với khóa học này. Hãy tải lại trang.');
      return;
    }
    this.progress.set(response.data);
  }
}

interface ProgressLoad {
  courseId: string | null;
  response: ApiEnvelope<StudentCourseProgress> | null;
  error: unknown | null;
}
