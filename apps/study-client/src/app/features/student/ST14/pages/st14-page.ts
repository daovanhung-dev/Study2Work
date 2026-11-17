import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ST14AttemptService } from '../data-access/st14-attempt.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentQuiz } from '../../shared/models/student-api.models';
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
  private quizId: string | null = null;
  readonly attemptId = signal<string | null>(null);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly saveError = signal<string | null>(null);
  readonly quiz = signal<StudentQuiz | null>(null);
  readonly currentQuestion = signal(0);
  readonly selected = signal<Record<number, number[]>>({});
  readonly savingQuestionId = signal<number | null>(null);
  readonly saved = signal(false);

  ngOnInit(): void {
    this.quizId = toSafeStudyId(this.route.snapshot.paramMap.get('quizId'));
    const attemptId = toSafeStudyId(this.route.snapshot.paramMap.get('attemptId'));
    this.attemptId.set(attemptId);
    if (!this.quizId || !attemptId) {
      this.error.set('Mã bài kiểm tra hoặc lượt làm không hợp lệ.');
      this.loading.set(false);
      return;
    }
    this.data.quiz(this.quizId).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else this.quiz.set(response.data);
        this.loading.set(false);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.loading.set(false);
      },
    });
  }

  isSelected(questionId: number, choiceId: number): boolean {
    return this.selected()[questionId]?.includes(choiceId) ?? false;
  }

  onChoiceChange(questionId: number, choiceId: number, event: Event): void {
    if (
      !(event.target instanceof HTMLInputElement) ||
      !this.attemptId() ||
      this.savingQuestionId() === questionId
    )
      return;
    const previous = this.selected()[questionId] ?? [];
    const next = event.target.checked
      ? [...previous, choiceId]
      : previous.filter((id) => id !== choiceId);
    this.selected.update((state) => ({ ...state, [questionId]: next }));
    this.savingQuestionId.set(questionId);
    this.saveError.set(null);
    this.saved.set(false);
    this.data.save(this.attemptId()!, questionId, next, '').subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) {
          this.selected.update((state) => ({ ...state, [questionId]: previous }));
          this.saveError.set(issue);
        } else this.saved.set(true);
        this.savingQuestionId.set(null);
      },
      error: (error: unknown) => {
        this.selected.update((state) => ({ ...state, [questionId]: previous }));
        this.saveError.set(studentApiErrorMessage(error));
        this.savingQuestionId.set(null);
      },
    });
  }

  previous(): void {
    this.currentQuestion.update((index) => Math.max(0, index - 1));
  }
  next(): void {
    this.currentQuestion.update((index) =>
      Math.min((this.quiz()?.questions.length ?? 1) - 1, index + 1),
    );
  }
}
