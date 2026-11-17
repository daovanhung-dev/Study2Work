import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ST19SubmissionService } from '../data-access/st19-submission.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentSubmission } from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [DatePipe, RouterLink],
  selector: 'study-st19-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    './st19-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st19-page.html',
})
export class ST19Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST19SubmissionService);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly submission = signal<StudentSubmission | null>(null);

  ngOnInit(): void {
    const submissionId = toSafeStudyId(this.route.snapshot.paramMap.get('submissionId'));
    if (!submissionId) {
      this.error.set('Mã bài nộp không hợp lệ.');
      this.loading.set(false);
      return;
    }
    this.data.submission(submissionId).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else this.submission.set(response.data);
        this.loading.set(false);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.loading.set(false);
      },
    });
  }
}
