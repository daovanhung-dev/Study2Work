import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { ST13QuizService } from '../data-access/st13-quiz.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentQuiz } from '../../shared/models/student-api.models';
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
  private quizId: string | null = null;
  readonly loading = signal(true);
  readonly starting = signal(false);
  readonly error = signal<string | null>(null);
  readonly quiz = signal<StudentQuiz | null>(null);

  ngOnInit(): void {
    this.quizId = toSafeStudyId(this.route.snapshot.paramMap.get('quizId'));
    if (!this.quizId) {
      this.error.set('Mã bài kiểm tra không hợp lệ.');
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

  start(): void {
    if (!this.quizId || this.starting() || !this.quiz()) return;
    this.starting.set(true);
    this.error.set(null);
    this.data.start(this.quizId).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        const attemptId = toSafeStudyId(response.data?.id);
        if (issue || !attemptId) {
          this.error.set(issue || 'Study Server không trả về mã lượt làm hợp lệ.');
          this.starting.set(false);
          return;
        }
        void this.router.navigate(['/student/quizzes', this.quizId, 'attempts', attemptId]);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.starting.set(false);
      },
    });
  }
}
