import { DatePipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { ST18SubmissionService } from '../data-access/st18-submission.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type {
  StudentAssignment,
  StudentSubmission,
  StudentUploadAsset,
} from '../../shared/models/student-api.models';
import { toSafeStudyId, toSafeStudyNumber } from '../../shared/models/student-api.models';

@Component({
  imports: [DatePipe, FormsModule, RouterLink],
  selector: 'study-st18-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    './st18-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st18-page.html',
})
export class ST18Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly data = inject(ST18SubmissionService);
  private readonly assignmentId = toSafeStudyId(this.route.snapshot.paramMap.get('assignmentId'));
  readonly assignment = signal<StudentAssignment | null>(null);
  readonly loading = signal(true);
  readonly busy = signal(false);
  readonly error = signal<string | null>(null);
  readonly content = signal('');
  readonly file = signal<File | null>(null);
  readonly uploadedAsset = signal<StudentUploadAsset | null>(null);
  readonly outcomeUnknown = signal(false);

  ngOnInit(): void {
    if (!this.assignmentId) {
      this.error.set('Mã bài tập không hợp lệ.');
      this.loading.set(false);
      return;
    }
    this.data.assignment(this.assignmentId).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else this.assignment.set(response.data);
        this.loading.set(false);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.loading.set(false);
      },
    });
  }

  selectFile(event: Event): void {
    const input = event.target;
    if (!(input instanceof HTMLInputElement)) return;
    this.file.set(input.files?.[0] ?? null);
    this.uploadedAsset.set(null);
    this.outcomeUnknown.set(false);
  }

  fileSize(bytes: number): string {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  }

  submit(): void {
    const assignment = this.assignment();
    if (!assignment || !this.assignmentId || this.busy() || this.outcomeUnknown()) return;
    const content = this.content().trim();
    if (!content && !this.file() && !this.uploadedAsset()) {
      this.error.set('Nhập nội dung hoặc đính kèm một tệp trước khi nộp.');
      return;
    }
    this.error.set(null);
    this.busy.set(true);
    const existingUploadId = toSafeStudyNumber(this.uploadedAsset()?.id);
    if (existingUploadId) {
      this.createSubmission(content, existingUploadId);
      return;
    }
    const file = this.file();
    if (!file) {
      this.createSubmission(content, null);
      return;
    }
    this.data.upload(file, assignment.course_id).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        const uploadId = toSafeStudyNumber(response.data?.id);
        if (issue || !uploadId) {
          this.error.set(issue || 'Upload chưa trả về mã tệp hợp lệ; chưa nộp bài.');
          this.busy.set(false);
          return;
        }
        this.uploadedAsset.set(response.data);
        this.createSubmission(content, uploadId);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.outcomeUnknown.set(error instanceof HttpErrorResponse && error.status === 0);
        this.busy.set(false);
      },
    });
  }

  private createSubmission(content: string, uploadId: number | null): void {
    this.data.submit(this.assignmentId!, content || null, uploadId).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        const submissionId = toSafeStudyId(response.data?.id);
        if (issue || !submissionId) {
          this.error.set(issue || 'Submission chưa trả về mã xác nhận hợp lệ.');
          this.busy.set(false);
          return;
        }
        void this.router.navigate(['/student/submissions', submissionId]);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.outcomeUnknown.set(error instanceof HttpErrorResponse && error.status === 0);
        this.busy.set(false);
      },
    });
  }
}
