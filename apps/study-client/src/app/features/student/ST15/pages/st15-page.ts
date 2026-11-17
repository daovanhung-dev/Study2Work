import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { StudentApiService, type QuizAttemptRecord } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st15-page',
  styleUrls: ['./st15-page.css', '../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st15-page.html',
})
export class ST15Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly api = inject(StudentApiService);

  readonly submission = new StudentApiState<QuizAttemptRecord>();
  attemptId = '';

  ngOnInit(): void {
    this.attemptId = this.route.snapshot.paramMap.get('attemptId') ?? '';
  }

  confirmSubmit(): void {
    if (!this.attemptId || this.submission.status() === 'loading') return;
    this.submission.load(this.api.submitAttempt(this.attemptId), (attempt) => {
      if (attempt?.id !== undefined && attempt?.id !== null) {
        void this.router.navigate(['/student/attempts', attempt.id, 'result']);
      }
    });
  }
}
