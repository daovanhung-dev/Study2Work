import { HttpErrorResponse } from '@angular/common/http';
import { Location } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { distinctUntilChanged, map, tap } from 'rxjs';

import { ST15SubmitService } from '../data-access/st15-submit.service';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import type { StudentQuizAttempt } from '../../shared/models/student-api.models';
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
export class ST15Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly location = inject(Location);
  private readonly data = inject(ST15SubmitService);
  private readonly destroyRef = inject(DestroyRef);
  readonly attemptId = signal(toSafeStudyId(this.route.snapshot.paramMap.get('attemptId')));
  readonly busy = signal(false);
  readonly error = signal<string | null>(null);
  readonly outcomeUnknownAttemptId = signal<string | null>(null);
  readonly resultCheckAttemptId = signal<string | null>(null);
  readonly submittedAttemptId = signal<string | null>(null);

  ngOnInit(): void {
    this.route.paramMap
      .pipe(
        map((params) => toSafeStudyId(params.get('attemptId'))),
        distinctUntilChanged(),
        tap((attemptId) => {
          this.attemptId.set(attemptId);
          this.error.set(
            attemptId ? null : 'Không tìm thấy lượt làm này.',
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe();
  }

  back(): void {
    this.location.back();
  }

  submit(): void {
    const attemptId = this.attemptId();
    if (
      !attemptId ||
      this.busy() ||
      this.outcomeUnknownAttemptId() === attemptId ||
      this.resultCheckAttemptId() === attemptId ||
      this.submittedAttemptId() === attemptId
    ) {
      return;
    }

    this.busy.set(true);
    this.error.set(null);
    // Keep the one-shot submit request alive until its committed attempt can be recovered.
    this.data.submit(attemptId).subscribe({
      next: (response) => {
        if (!response.success) {
          if (this.attemptId() === attemptId) {
            this.error.set('Chưa thể nộp bài kiểm tra. Vui lòng thử lại.');
          }
          if (response.businessCode === 'DESIGN_STATE_CONFLICT') {
            this.resultCheckAttemptId.set(attemptId);
          }
          this.busy.set(false);
          return;
        }
        if (
          response.businessCode !== 'DESIGN_RESOURCE_UPDATED' ||
          !isSubmittedAttempt(response.data, attemptId)
        ) {
          if (this.attemptId() === attemptId) {
            this.error.set('Chưa thể xác nhận bài đã được nộp. Hãy kiểm tra kết quả.');
          }
          this.outcomeUnknownAttemptId.set(attemptId);
          this.resultCheckAttemptId.set(attemptId);
          this.busy.set(false);
          return;
        }

        this.submittedAttemptId.set(attemptId);
        if (this.destroyRef.destroyed || this.attemptId() !== attemptId) {
          this.busy.set(false);
          return;
        }
        void this.router
          .navigate(['/student/attempts', attemptId, 'result'])
          .then((navigated) => {
            this.busy.set(false);
            if (!navigated) {
              this.error.set('Bài đã được nộp. Mở trang kết quả bằng liên kết bên dưới.');
            }
          })
          .catch(() => {
            this.busy.set(false);
            this.error.set('Bài đã được nộp. Mở trang kết quả bằng liên kết bên dưới.');
          });
      },
      error: (error: unknown) => {
        const status = error instanceof HttpErrorResponse ? error.status : null;
        if (this.attemptId() === attemptId) {
          this.error.set(studentApiErrorMessage(error));
        }
        if (status === 0) {
          this.outcomeUnknownAttemptId.set(attemptId);
          this.resultCheckAttemptId.set(attemptId);
        } else if (status === 409) {
          this.resultCheckAttemptId.set(attemptId);
        }
        this.busy.set(false);
      },
    });
  }
}

function isSubmittedAttempt(value: unknown, attemptId: string): value is StudentQuizAttempt {
  if (typeof value !== 'object' || value === null) return false;
  const attempt = value as Record<string, unknown>;
  return (
    toSafeStudyId(attempt['id']) === attemptId &&
    toSafeStudyId(attempt['quiz_id']) !== null &&
    attempt['status'] === 'GRADED' &&
    typeof attempt['started_at'] === 'string' &&
    typeof attempt['submitted_at'] === 'string' &&
    (typeof attempt['score'] === 'string' || typeof attempt['score'] === 'number') &&
    typeof attempt['passed'] === 'boolean' &&
    Array.isArray(attempt['answers'])
  );
}
