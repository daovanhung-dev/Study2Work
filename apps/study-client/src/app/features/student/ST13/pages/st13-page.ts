import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { StudentApiService, type QuizAttemptRecord, type QuizRecord } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st13-page',
  styleUrls: ['./st13-page.css', './st13-icons.css', '../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st13-page.html',
})
export class ST13Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly api = inject(StudentApiService);

  readonly quiz = new StudentApiState<QuizRecord>();
  readonly attempt = new StudentApiState<QuizAttemptRecord>();
  quizId = '';

  ngOnInit(): void {
    this.quizId = this.route.snapshot.paramMap.get('quizId') ?? '';
    if (this.quizId) this.quiz.load(this.api.getQuiz(this.quizId));
  }

  startAttempt(): void {
    if (!this.quizId || this.attempt.status() === 'loading') return;
    this.attempt.load(this.api.startAttempt(this.quizId), (attempt) => {
      if (attempt?.id !== undefined && attempt?.id !== null) {
        void this.router.navigate(['/student/quizzes', this.quizId, 'attempts', attempt.id]);
      }
    });
  }
}
