import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, computed, inject, signal } from '@angular/core';
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

import { ST11LessonService } from '../data-access/st11-lesson.service';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import type { StudentLesson } from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [RouterLink],
  selector: 'study-st11-page',
  styleUrls: [
    './st11-page.css',
    '../../../../shared/ui/student-static-screen.css',
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
  ],
  templateUrl: './st11-page.html',
})
export class ST11Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST11LessonService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly retryLesson$ = new Subject<void>();
  private loadGeneration = 0;

  readonly lessonId = signal(toSafeStudyId(this.route.snapshot.paramMap.get('lessonId')));
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly lesson = signal<StudentLesson | null>(null);

  readonly progressBusy = signal(false);
  readonly progressSaved = signal(false);
  readonly progressError = signal<string | null>(null);

  readonly nextLoading = signal(false);
  readonly nextLesson = signal<StudentLesson | null>(null);
  readonly nextEndOfCourse = signal(false);
  readonly nextError = signal<string | null>(null);

  readonly safeVideoUrl = computed(() => toSafeHttpUrl(this.lesson()?.video_url));
  readonly nextLessonId = computed(() => {
    const next = this.nextLesson();
    return next ? toSafeStudyId(next.id) : null;
  });

  ngOnInit(): void {
    const lessonId$ = this.route.paramMap.pipe(
      map((params) => toSafeStudyId(params.get('lessonId'))),
      distinctUntilChanged(),
      tap((lessonId) => this.lessonId.set(lessonId)),
    );

    combineLatest([lessonId$, this.retryLesson$.pipe(startWith(undefined))])
      .pipe(
        tap(() => {
          this.loadGeneration += 1;
          this.loading.set(true);
          this.error.set(null);
          this.lesson.set(null);
          this.progressBusy.set(false);
          this.progressSaved.set(false);
          this.progressError.set(null);
          this.nextLoading.set(false);
          this.nextLesson.set(null);
          this.nextEndOfCourse.set(false);
          this.nextError.set(null);
        }),
        switchMap(([lessonId]) => this.loadLesson(lessonId)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyLessonResult(result));
  }

  retryLesson(): void {
    this.retryLesson$.next();
  }

  markCompleted(): void {
    const lessonId = this.lessonId();
    if (!lessonId || this.progressBusy()) return;
    const generation = this.loadGeneration;
    this.progressBusy.set(true);
    this.progressError.set(null);
    this.data
      .updateProgress(lessonId, { percent: 100, completed: true })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          if (generation !== this.loadGeneration) return;
          this.progressBusy.set(false);
          if (response.success && response.businessCode === 'DESIGN_RESOURCE_UPDATED') {
            this.progressSaved.set(true);
          } else {
            this.progressError.set('Chưa thể ghi nhận tiến độ bài học. Vui lòng thử lại.');
          }
        },
        error: (error: unknown) => {
          if (generation !== this.loadGeneration) return;
          this.progressBusy.set(false);
          this.progressError.set(studentApiErrorMessage(error));
        },
      });
  }

  lessonStatusLabel(status: string): string {
    return status === 'PUBLISHED' ? 'Đã xuất bản' : 'Trạng thái chưa hỗ trợ';
  }

  private loadLesson(lessonId: string | null) {
    if (!lessonId) return of({ lessonId, response: null, error: null });
    return this.data.lesson(lessonId).pipe(
      map((response) => ({ lessonId, response, error: null })),
      catchError((error: unknown) => of({ lessonId, response: null, error })),
    );
  }

  private applyLessonResult(result: LessonResult): void {
    this.loading.set(false);
    if (!result.lessonId) {
      this.error.set('Không tìm thấy bài học này.');
      return;
    }
    if (result.error !== null) {
      this.error.set(studentApiErrorMessage(result.error));
      return;
    }

    const response = result.response;
    if (!response?.success || response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
      this.error.set('Chưa thể tải nội dung bài học. Vui lòng thử lại.');
      return;
    }
    if (!isStudentLesson(response.data)) {
      this.error.set('Thông tin bài học chưa đúng định dạng. Hãy tải lại trang.');
      return;
    }
    if (toSafeStudyId(response.data.id) !== result.lessonId) {
      this.error.set('Không tìm thấy bài học này.');
      return;
    }
    this.lesson.set(response.data);
    this.loadNextLesson(result.lessonId, this.loadGeneration);
  }

  private loadNextLesson(lessonId: string, generation: number): void {
    this.nextLoading.set(true);
    this.data
      .nextLesson(lessonId)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          if (generation !== this.loadGeneration) return;
          this.nextLoading.set(false);
          if (
            response.success &&
            response.businessCode === 'DESIGN_RESOURCE_RETRIEVED' &&
            isStudentLesson(response.data)
          ) {
            this.nextLesson.set(response.data);
          } else {
            this.nextEndOfCourse.set(true);
          }
        },
        error: (error: unknown) => {
          if (generation !== this.loadGeneration) return;
          this.nextLoading.set(false);
          if (error instanceof HttpErrorResponse && error.status === 404) {
            this.nextEndOfCourse.set(true);
          } else {
            this.nextError.set(studentApiErrorMessage(error));
          }
        },
      });
  }
}

interface LessonResult {
  lessonId: string | null;
  response: ApiEnvelope<StudentLesson> | null;
  error: unknown | null;
}

function toSafeHttpUrl(value: string | null | undefined): string | null {
  if (!value) return null;
  try {
    const parsed = new URL(value);
    return parsed.protocol === 'https:' || parsed.protocol === 'http:' ? parsed.toString() : null;
  } catch {
    return null;
  }
}

function isStudentLesson(value: unknown): value is StudentLesson {
  if (typeof value !== 'object' || value === null) return false;
  const lesson = value as Record<string, unknown>;
  return (
    typeof lesson['id'] === 'number' &&
    Number.isSafeInteger(lesson['id']) &&
    lesson['id'] > 0 &&
    typeof lesson['course_id'] === 'number' &&
    Number.isSafeInteger(lesson['course_id']) &&
    lesson['course_id'] > 0 &&
    typeof lesson['title'] === 'string' &&
    typeof lesson['order'] === 'number' &&
    typeof lesson['status'] === 'string'
  );
}
