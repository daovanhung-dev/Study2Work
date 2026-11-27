import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
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

import { ST13QuizService } from '../data-access/st13-quiz.service';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import type {
  StudentQuiz,
  StudentQuizAttempt,
  StudentQuizQuestion,
} from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [RouterLink],
  selector: 'study-st13-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    './st13-page.css',
    './st13-icons.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st13-page.html',
})
export class ST13Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly data = inject(ST13QuizService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly retryQuiz$ = new Subject<void>();
  readonly quizId = signal(toSafeStudyId(this.route.snapshot.paramMap.get('quizId')));
  readonly loading = signal(true);
  readonly starting = signal(false);
  readonly error = signal<string | null>(null);
  readonly startError = signal<string | null>(null);
  readonly quiz = signal<StudentQuiz | null>(null);
  readonly createdAttemptQuizId = signal<string | null>(null);
  readonly createdAttemptId = signal<string | null>(null);
  readonly startBlockedQuizId = signal<string | null>(null);

  ngOnInit(): void {
    const quizId$ = this.route.paramMap.pipe(
      map((params) => toSafeStudyId(params.get('quizId'))),
      distinctUntilChanged(),
      tap((quizId) => {
        this.quizId.set(quizId);
        this.startError.set(null);
      }),
    );

    combineLatest([quizId$, this.retryQuiz$.pipe(startWith(undefined))])
      .pipe(
        tap(() => {
          this.loading.set(true);
          this.error.set(null);
          this.quiz.set(null);
        }),
        switchMap(([quizId]) => this.loadQuiz(quizId)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyQuizResult(result));
  }

  retryQuiz(): void {
    this.retryQuiz$.next();
  }

  start(): void {
    const quizId = this.quizId();
    if (
      !quizId ||
      this.starting() ||
      !this.quiz() ||
      this.createdAttemptQuizId() === quizId ||
      this.startBlockedQuizId() === quizId
    ) {
      return;
    }

    this.starting.set(true);
    this.startError.set(null);
    // Keep the one-shot mutation alive until its attempt ID can be routed or recovered.
    this.data.start(quizId).subscribe({
      next: (response) => {
        if (!response.success) {
          this.blockStart(quizId);
          return;
        }
        if (response.businessCode !== 'DESIGN_RESOURCE_CREATED') {
          this.blockStart(quizId);
          return;
        }
        if (
          !isStudentQuizAttempt(response.data) ||
          toSafeStudyId(response.data.quiz_id) !== quizId
        ) {
          this.blockStart(quizId);
          return;
        }

        const attemptId = toSafeStudyId(response.data.id);
        if (!attemptId) {
          this.blockStart(quizId);
          return;
        }

        this.createdAttemptQuizId.set(quizId);
        this.createdAttemptId.set(attemptId);
        void this.router
          .navigate(['/student/quizzes', quizId, 'attempts', attemptId])
          .then((navigated) => {
            this.starting.set(false);
            if (!navigated) {
              this.startError.set(
                'Lượt làm đã được tạo. Dùng liên kết bên dưới để tiếp tục lượt làm này.',
              );
            }
          })
          .catch(() => {
            this.starting.set(false);
            this.startError.set(
              'Lượt làm đã được tạo. Dùng liên kết bên dưới để tiếp tục lượt làm này.',
            );
          });
      },
      error: (error: unknown) => {
        if (
          error instanceof HttpErrorResponse &&
          (error.status === 0 || error.status === 409 || error.status >= 500)
        ) {
          this.blockStart(quizId);
          return;
        }
        this.startError.set(
          studentApiErrorMessage(error),
        );
        this.starting.set(false);
      },
    });
  }

  private loadQuiz(quizId: string | null) {
    if (!quizId) return of({ quizId, response: null, error: null });
    return this.data.quiz(quizId).pipe(
      map((response) => ({ quizId, response, error: null })),
      catchError((error: unknown) => of({ quizId, response: null, error })),
    );
  }

  private blockStart(quizId: string): void {
    this.startBlockedQuizId.set(quizId);
    this.startError.set(
      'Không xác định được lượt làm nào để tiếp tục. Nút bắt đầu đã khóa để tránh tạo lượt trùng.',
    );
    this.starting.set(false);
  }

  private applyQuizResult(result: QuizResult): void {
    this.loading.set(false);
    if (!result.quizId) {
      this.error.set('Không tìm thấy bài kiểm tra này.');
      return;
    }
    if (result.error !== null) {
      this.error.set(studentApiErrorMessage(result.error));
      return;
    }

    const response = result.response;
    if (!response?.success) {
      this.error.set('Chưa thể tải thông tin bài kiểm tra. Vui lòng thử lại.');
      return;
    }
    if (response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
      this.error.set('Chưa thể tải thông tin bài kiểm tra. Vui lòng thử lại.');
      return;
    }
    if (!isStudentQuiz(response.data) || toSafeStudyId(response.data.id) !== result.quizId) {
      this.error.set('Thông tin bài kiểm tra chưa đúng định dạng. Hãy tải lại trang.');
      return;
    }
    this.quiz.set(response.data);
  }
}

interface QuizResult {
  quizId: string | null;
  response: ApiEnvelope<StudentQuiz> | null;
  error: unknown | null;
}

function isStudentQuiz(value: unknown): value is StudentQuiz {
  if (typeof value !== 'object' || value === null) return false;
  const quiz = value as Record<string, unknown>;
  const duration = quiz['duration_minutes'];
  return (
    toSafeStudyId(quiz['id']) !== null &&
    toSafeStudyId(quiz['course_id']) !== null &&
    typeof quiz['title'] === 'string' &&
    (duration === null ||
      duration === undefined ||
      (typeof duration === 'number' && Number.isInteger(duration) && duration > 0)) &&
    typeof quiz['passing_score'] === 'string' &&
    Array.isArray(quiz['questions']) &&
    quiz['questions'].every(isStudentQuizQuestion)
  );
}

function isStudentQuizQuestion(value: unknown): value is StudentQuizQuestion {
  if (typeof value !== 'object' || value === null) return false;
  const question = value as Record<string, unknown>;
  return (
    toSafeStudyId(question['id']) !== null &&
    typeof question['text'] === 'string' &&
    question['type'] === 'MULTIPLE_CHOICE' &&
    Array.isArray(question['choices']) &&
    question['choices'].every((choice: unknown) => {
      if (typeof choice !== 'object' || choice === null) return false;
      const item = choice as Record<string, unknown>;
      return toSafeStudyId(item['id']) !== null && typeof item['choice_text'] === 'string';
    })
  );
}

function isStudentQuizAttempt(value: unknown): value is StudentQuizAttempt {
  if (typeof value !== 'object' || value === null) return false;
  const attempt = value as Record<string, unknown>;
  return (
    toSafeStudyId(attempt['id']) !== null &&
    toSafeStudyId(attempt['quiz_id']) !== null &&
    attempt['status'] === 'IN_PROGRESS' &&
    typeof attempt['started_at'] === 'string' &&
    Array.isArray(attempt['answers'])
  );
}
