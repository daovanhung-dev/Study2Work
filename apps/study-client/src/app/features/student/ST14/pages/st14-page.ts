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

import { ST14AttemptService } from '../data-access/st14-attempt.service';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import type {
  StudentQuiz,
  StudentQuizAnswer,
  StudentQuizQuestion,
} from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [RouterLink],
  selector: 'study-st14-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    './st14-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st14-page.html',
})
export class ST14Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST14AttemptService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly retryQuiz$ = new Subject<void>();
  private saveGeneration = 0;
  readonly quizId = signal<string | null>(
    toSafeStudyId(this.route.snapshot.paramMap.get('quizId')),
  );
  readonly attemptId = signal<string | null>(
    toSafeStudyId(this.route.snapshot.paramMap.get('attemptId')),
  );
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly saveError = signal<string | null>(null);
  readonly quiz = signal<StudentQuiz | null>(null);
  readonly currentQuestion = signal(0);
  readonly selected = signal<Record<number, number[]>>({});
  readonly savingQuestionId = signal<number | null>(null);
  readonly saved = signal(false);

  ngOnInit(): void {
    const routeIds$ = this.route.paramMap.pipe(
      map((params) => ({
        quizId: toSafeStudyId(params.get('quizId')),
        attemptId: toSafeStudyId(params.get('attemptId')),
      })),
      distinctUntilChanged(
        (previous, current) =>
          previous.quizId === current.quizId && previous.attemptId === current.attemptId,
      ),
      tap(({ quizId, attemptId }) => {
        this.quizId.set(quizId);
        this.attemptId.set(attemptId);
        this.saveGeneration += 1;
        this.currentQuestion.set(0);
        this.selected.set({});
        this.savingQuestionId.set(null);
        this.saved.set(false);
        this.saveError.set(null);
      }),
    );

    combineLatest([routeIds$, this.retryQuiz$.pipe(startWith(undefined))])
      .pipe(
        tap(() => {
          this.loading.set(true);
          this.error.set(null);
          this.quiz.set(null);
        }),
        switchMap(([routeIds]) => this.loadQuiz(routeIds.quizId, routeIds.attemptId)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyQuizResult(result));
  }

  retryQuiz(): void {
    this.retryQuiz$.next();
  }

  isSelected(questionId: number, choiceId: number): boolean {
    return this.selected()[questionId]?.includes(choiceId) ?? false;
  }

  onChoiceChange(questionId: number, choiceId: number, event: Event): void {
    if (!(event.target instanceof HTMLInputElement)) return;

    if (
      !this.attemptId() ||
      !this.quizId() ||
      !this.quiz() ||
      this.savingQuestionId() !== null
    ) {
      event.target.checked = this.isSelected(questionId, choiceId);
      return;
    }

    const attemptId = this.attemptId()!;
    const quizId = this.quizId()!;
    const quiz = this.quiz()!;
    const question = quiz.questions.find((item) => item.id === questionId);
    if (!question?.choices.some((choice) => choice.id === choiceId)) {
      event.target.checked = this.isSelected(questionId, choiceId);
      return;
    }

    const previous = this.selected()[questionId] ?? [];
    const next = event.target.checked
      ? [...previous, choiceId]
      : previous.filter((id) => id !== choiceId);
    this.selected.update((state) => ({ ...state, [questionId]: next }));
    this.savingQuestionId.set(questionId);
    this.saveError.set(null);
    this.saved.set(false);
    const requestGeneration = ++this.saveGeneration;

    this.data.save(attemptId, questionId, next).subscribe({
      next: (response) => {
        if (!this.isCurrentSave(quizId, attemptId, requestGeneration)) return;

        if (!response.success) {
          this.rollbackAnswer(questionId, previous, 'Câu trả lời chưa được lưu. Vui lòng thử lại.');
          return;
        }
        if (response.businessCode !== 'DESIGN_RESOURCE_UPDATED') {
          this.rollbackAnswer(questionId, previous, 'Chưa thể lưu câu trả lời. Vui lòng thử lại.');
          return;
        }
        if (!isStudentQuizAttempt(response.data, attemptId, quizId)) {
          this.rollbackAnswer(questionId, previous, 'Thông tin lượt làm chưa hợp lệ. Hãy tải lại trang.');
          return;
        }

        const savedAnswers = toSelectedAnswers(response.data.answers, quiz);
        if (!savedAnswers) {
          this.rollbackAnswer(questionId, previous, 'Câu trả lời chưa khớp với bài kiểm tra. Hãy tải lại trang.');
          return;
        }
        this.selected.set(savedAnswers);
        this.saved.set(true);
        this.savingQuestionId.set(null);
      },
      error: (error: unknown) => {
        if (!this.isCurrentSave(quizId, attemptId, requestGeneration)) return;
        this.rollbackAnswer(questionId, previous, studentApiErrorMessage(error));
      },
    });
  }

  previous(): void {
    this.currentQuestion.update((index) => Math.max(0, index - 1));
    this.saved.set(false);
  }

  next(): void {
    const questionCount = this.quiz()?.questions.length ?? 0;
    if (questionCount === 0) return;
    this.currentQuestion.update((index) => Math.min(questionCount - 1, index + 1));
    this.saved.set(false);
  }

  selectQuestion(index: number): void {
    const questionCount = this.quiz()?.questions.length ?? 0;
    if (index < 0 || index >= questionCount) return;
    this.currentQuestion.set(index);
    this.saved.set(false);
  }

  private loadQuiz(quizId: string | null, attemptId: string | null) {
    if (!quizId || !attemptId) return of({ quizId, attemptId, response: null, error: null });
    return this.data.quiz(quizId).pipe(
      map((response) => ({ quizId, attemptId, response, error: null })),
      catchError((error: unknown) => of({ quizId, attemptId, response: null, error })),
    );
  }

  private applyQuizResult(result: QuizResult): void {
    this.loading.set(false);
    if (!result.quizId || !result.attemptId) {
      this.error.set('Không tìm thấy bài kiểm tra này.');
      return;
    }
    if (result.error !== null) {
      this.error.set(studentApiErrorMessage(result.error));
      return;
    }

    const response = result.response;
    if (!response?.success) {
      this.error.set('Chưa thể tải nội dung bài kiểm tra. Vui lòng thử lại.');
      return;
    }
    if (response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
      this.error.set('Chưa thể tải nội dung bài kiểm tra. Vui lòng thử lại.');
      return;
    }
    if (!isStudentQuiz(response.data) || toSafeStudyId(response.data.id) !== result.quizId) {
      this.error.set('Thông tin bài kiểm tra chưa đúng định dạng. Hãy tải lại trang.');
      return;
    }
    this.quiz.set(response.data);
  }

  private isCurrentSave(quizId: string, attemptId: string, generation: number): boolean {
    return (
      this.quizId() === quizId &&
      this.attemptId() === attemptId &&
      this.saveGeneration === generation
    );
  }

  private rollbackAnswer(questionId: number, previous: number[], message: string): void {
    this.selected.update((state) => ({ ...state, [questionId]: previous }));
    this.saveError.set(message);
    this.savingQuestionId.set(null);
  }
}

interface QuizResult {
  quizId: string | null;
  attemptId: string | null;
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
      (typeof duration === 'number' && Number.isInteger(duration))) &&
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

function isStudentQuizAttempt(
  value: unknown,
  attemptId: string,
  quizId: string,
): value is { id: number; quiz_id: number; status: string; answers: StudentQuizAnswer[] } {
  if (typeof value !== 'object' || value === null) return false;
  const attempt = value as Record<string, unknown>;
  return (
    toSafeStudyId(attempt['id']) === attemptId &&
    toSafeStudyId(attempt['quiz_id']) === quizId &&
    attempt['status'] === 'IN_PROGRESS' &&
    typeof attempt['started_at'] === 'string' &&
    Array.isArray(attempt['answers']) &&
    attempt['answers'].every(isStudentQuizAnswer)
  );
}

function isStudentQuizAnswer(value: unknown): value is StudentQuizAnswer {
  if (typeof value !== 'object' || value === null) return false;
  const answer = value as Record<string, unknown>;
  return (
    toSafeStudyId(answer['question_id']) !== null &&
    Array.isArray(answer['choice_ids']) &&
    answer['choice_ids'].every((choiceId: unknown) => toSafeStudyId(choiceId) !== null) &&
    (answer['text_answer'] === undefined ||
      answer['text_answer'] === null ||
      typeof answer['text_answer'] === 'string')
  );
}

function toSelectedAnswers(
  answers: StudentQuizAnswer[],
  quiz: StudentQuiz,
): Record<number, number[]> | null {
  const questions = new Map(
    quiz.questions.map((question) => [toSafeStudyId(question.id), question] as const),
  );
  const selected: Record<number, number[]> = {};

  for (const answer of answers) {
    const questionId = toSafeStudyId(answer.question_id);
    if (!questionId) return null;
    const question = questions.get(questionId);
    if (!question) return null;
    const availableChoices = new Set(question.choices.map((choice) => toSafeStudyId(choice.id)));
    const choiceIds = answer.choice_ids ?? [];
    if (choiceIds.some((choiceId) => !availableChoices.has(toSafeStudyId(choiceId)))) return null;
    selected[Number(questionId)] = choiceIds;
  }
  return selected;
}
