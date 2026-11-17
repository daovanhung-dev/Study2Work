import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import {
  StudentApiService,
  type ApiId,
  type QuizAttemptRecord,
  type QuizQuestion,
  type QuizRecord,
} from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st14-page',
  styleUrls: ['./st14-page.css', './st14-navigation.css', '../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st14-page.html',
})
export class ST14Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly api = inject(StudentApiService);

  readonly quiz = new StudentApiState<QuizRecord>();
  readonly answerSave = new StudentApiState<QuizAttemptRecord>();
  quizId = '';
  attemptId = '';
  currentQuestionIndex = 0;
  selectedChoices: Record<string, ApiId[]> = {};

  ngOnInit(): void {
    this.quizId = this.route.snapshot.paramMap.get('quizId') ?? '';
    this.attemptId = this.route.snapshot.paramMap.get('attemptId') ?? '';
    if (this.quizId) this.quiz.load(this.api.getQuiz(this.quizId));
  }

  toggleChoice(questionId: ApiId, choiceId: ApiId, event: Event): void {
    const checked = (event.currentTarget as HTMLInputElement | null)?.checked === true;
    const key = String(questionId);
    const current = this.selectedChoices[key] ?? [];
    const next = checked ? [...current.filter((id) => String(id) !== String(choiceId)), choiceId] : current.filter((id) => String(id) !== String(choiceId));
    this.selectedChoices = { ...this.selectedChoices, [key]: next };
    if (this.attemptId) this.answerSave.load(this.api.saveAnswer(this.attemptId, questionId, next));
  }

  choiceSelected(questionId: ApiId, choiceId: ApiId): boolean {
    return this.selectedChoices[String(questionId)]?.some((id) => String(id) === String(choiceId)) ?? false;
  }

  get currentQuestion(): QuizQuestion | null {
    return this.quiz.data()?.questions[this.currentQuestionIndex] ?? null;
  }

  selectQuestion(index: number): void {
    const questionCount = this.quiz.data()?.questions.length ?? 0;
    if (!Number.isInteger(index) || index < 0 || index >= questionCount) return;
    this.currentQuestionIndex = index;
  }

  previousQuestion(): void {
    this.selectQuestion(this.currentQuestionIndex - 1);
  }

  nextQuestion(): void {
    this.selectQuestion(this.currentQuestionIndex + 1);
  }

  continueToSubmit(): void {
    if (this.attemptId) void this.router.navigate(['/student/attempts', this.attemptId, 'submit']);
  }
}
