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
  readonly lessonId = signal(toSafeStudyId(this.route.snapshot.paramMap.get('lessonId')));
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly lesson = signal<StudentLesson | null>(null);

  ngOnInit(): void {
    const lessonId$ = this.route.paramMap.pipe(
      map((params) => toSafeStudyId(params.get('lessonId'))),
      distinctUntilChanged(),
      tap((lessonId) => this.lessonId.set(lessonId)),
    );

    combineLatest([lessonId$, this.retryLesson$.pipe(startWith(undefined))])
      .pipe(
        tap(() => {
          this.loading.set(true);
          this.error.set(null);
          this.lesson.set(null);
        }),
        switchMap(([lessonId]) => this.loadLesson(lessonId)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyLessonResult(result));
  }

  retryLesson(): void {
    this.retryLesson$.next();
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
    if (!response?.success) {
      this.error.set('Chưa thể tải nội dung bài học. Vui lòng thử lại.');
      return;
    }
    if (response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
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
  }
}

interface LessonResult {
  lessonId: string | null;
  response: ApiEnvelope<StudentLesson> | null;
  error: unknown | null;
}

function isStudentLesson(value: unknown): value is StudentLesson {
  if (typeof value !== 'object' || value === null) return false;
  const lesson = value as Record<string, unknown>;
  return (
    toSafeStudyId(lesson['id']) !== null &&
    toSafeStudyId(lesson['course_id']) !== null &&
    typeof lesson['title'] === 'string' &&
    typeof lesson['order'] === 'number' &&
    Number.isInteger(lesson['order']) &&
    lesson['status'] === 'PUBLISHED' &&
    (lesson['content'] === undefined ||
      lesson['content'] === null ||
      typeof lesson['content'] === 'string') &&
    (lesson['video_url'] === undefined ||
      lesson['video_url'] === null ||
      typeof lesson['video_url'] === 'string')
  );
}
