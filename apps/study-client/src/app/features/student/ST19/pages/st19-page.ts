import { DatePipe } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import {
  Subject,
  catchError,
  combineLatest,
  distinctUntilChanged,
  map,
  of,
  startWith,
  switchMap,
  tap,
} from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ST19SubmissionService } from '../data-access/st19-submission.service';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import type { StudentSubmission } from '../../shared/models/student-api.models';
import { toSafeStudyId, toSafeStudyNumber } from '../../shared/models/student-api.models';

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
  private readonly destroyRef = inject(DestroyRef);
  private readonly retrySubmission$ = new Subject<void>();
  readonly submissionId = signal(toSafeStudyId(this.route.snapshot.paramMap.get('submissionId')));
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly submission = signal<StudentSubmission | null>(null);

  ngOnInit(): void {
    const submissionId$ = this.route.paramMap.pipe(
      map((params) => toSafeStudyId(params.get('submissionId'))),
      distinctUntilChanged(),
      tap((submissionId) => this.submissionId.set(submissionId)),
    );

    combineLatest([submissionId$, this.retrySubmission$.pipe(startWith(undefined))])
      .pipe(
        tap(() => {
          this.loading.set(true);
          this.error.set(null);
          this.submission.set(null);
        }),
        switchMap(([submissionId]) => this.loadSubmission(submissionId)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applySubmission(result));
  }

  retrySubmission(): void {
    this.retrySubmission$.next();
  }

  isGraded(status: string): boolean {
    return status.toUpperCase() === 'GRADED';
  }

  submissionStatusLabel(status: string): string {
    switch (status.toUpperCase()) {
      case 'SUBMITTED':
        return 'Đã nộp';
      case 'GRADED':
        return 'Đã chấm';
      default:
        return 'Trạng thái chưa được hỗ trợ';
    }
  }

  private loadSubmission(submissionId: string | null) {
    if (!submissionId) return of({ submissionId, response: null, error: null });
    return this.data.submission(submissionId).pipe(
      map((response) => ({ submissionId, response, error: null })),
      catchError((error: unknown) => of({ submissionId, response: null, error })),
    );
  }

  private applySubmission(result: SubmissionLoad): void {
    this.loading.set(false);
    if (!result.submissionId) {
      this.error.set('Không tìm thấy bài nộp này.');
      return;
    }
    if (result.error !== null) {
      this.error.set(studentApiErrorMessage(result.error));
      return;
    }

    const response = result.response;
    if (!response?.success) {
      this.error.set('Chưa thể tải bài nộp. Vui lòng thử lại.');
      return;
    }
    if (
      response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isStudentSubmission(response.data, result.submissionId)
    ) {
      this.error.set('Thông tin bài nộp không khớp. Hãy tải lại trang.');
      return;
    }
    this.submission.set(response.data);
  }
}

interface SubmissionLoad {
  submissionId: string | null;
  response: ApiEnvelope<StudentSubmission> | null;
  error: unknown | null;
}

function isStudentSubmission(value: unknown, submissionId: string): value is StudentSubmission {
  if (typeof value !== 'object' || value === null) return false;
  const submission = value as Record<string, unknown>;
  return (
    toSafeStudyId(submission['id']) === submissionId &&
    toSafeStudyId(submission['assignment_id']) !== null &&
    toSafeStudyId(submission['user_id']) !== null &&
    (submission['content'] === undefined ||
      submission['content'] === null ||
      typeof submission['content'] === 'string') &&
    Array.isArray(submission['files']) &&
    submission['files'].every((file: unknown) => isStudentSubmissionFile(file)) &&
    typeof submission['status'] === 'string' &&
    typeof submission['submitted_at'] === 'string' &&
    (submission['score'] === undefined ||
      submission['score'] === null ||
      typeof submission['score'] === 'string' ||
      typeof submission['score'] === 'number') &&
    (submission['feedback'] === undefined ||
      submission['feedback'] === null ||
      typeof submission['feedback'] === 'string')
  );
}

function isStudentSubmissionFile(value: unknown): boolean {
  if (typeof value !== 'object' || value === null) return false;
  const file = value as Record<string, unknown>;
  return (
    toSafeStudyNumber(file['id']) !== null &&
    typeof file['name'] === 'string' &&
    typeof file['url'] === 'string' &&
    typeof file['content_type'] === 'string' &&
    typeof file['size_bytes'] === 'number' &&
    typeof file['status'] === 'string'
  );
}
