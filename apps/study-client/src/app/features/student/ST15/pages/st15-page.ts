import { HttpErrorResponse } from '@angular/common/http';
import { Location } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { ST15SubmitService } from '../data-access/st15-submit.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [RouterLink],
  selector: 'study-st15-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    './st15-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st15-page.html',
})
export class ST15Page {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly location = inject(Location);
  private readonly data = inject(ST15SubmitService);
  readonly attemptId = toSafeStudyId(this.route.snapshot.paramMap.get('attemptId'));
  readonly busy = signal(false);
  readonly error = signal<string | null>(null);
  readonly outcomeUnknown = signal(false);

  back(): void {
    this.location.back();
  }

  submit(): void {
    if (!this.attemptId || this.busy() || this.outcomeUnknown()) return;
    this.busy.set(true);
    this.error.set(null);
    this.data.submit(this.attemptId).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) {
          this.error.set(issue);
          this.busy.set(false);
          return;
        }
        void this.router.navigate(['/student/attempts', this.attemptId, 'result']);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.outcomeUnknown.set(error instanceof HttpErrorResponse && error.status === 0);
        this.busy.set(false);
      },
    });
  }
}
