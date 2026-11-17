import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ST16ResultService } from '../data-access/st16-result.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentQuizAttempt } from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [DatePipe, RouterLink],
  selector: 'study-st16-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    './st16-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st16-page.html',
})
export class ST16Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST16ResultService);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly result = signal<StudentQuizAttempt | null>(null);
  readonly attemptId = toSafeStudyId(this.route.snapshot.paramMap.get('attemptId'));

  ngOnInit(): void {
    if (!this.attemptId) {
      this.error.set('Mã lượt làm không hợp lệ.');
      this.loading.set(false);
      return;
    }
    this.data.result(this.attemptId).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else this.result.set(response.data);
        this.loading.set(false);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.loading.set(false);
      },
    });
  }
}
