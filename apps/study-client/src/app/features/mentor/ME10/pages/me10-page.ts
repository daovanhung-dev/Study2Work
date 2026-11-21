import { DatePipe } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import {
  EMPTY,
  Subject,
  catchError,
  distinctUntilChanged,
  map,
  of,
  startWith,
  switchMap,
  tap,
} from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ME10SubmissionReviewService } from '../data-access/me10-submission-review.service';
import type { MentorSubmission } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

type ME10LoadResult =
  | { submissionId: string; response: ApiEnvelope<MentorSubmission> }
  | { submissionId: string; error: unknown };

@Component({
  imports: [DatePipe, RouterLink, MentorPageHeader],
  selector: 'study-me10-page',
  styleUrls: ['./me10-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me10-page.html',
})
export class ME10Page implements OnInit {
  private readonly data = inject(ME10SubmissionReviewService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly route = inject(ActivatedRoute);
  private readonly retry$ = new Subject<void>();

  readonly submissionId = signal('');
  readonly submission = signal<MentorSubmission | null>(null);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly invalidId = signal(false);
  readonly notFound = signal(false);
  readonly forbidden = signal(false);

  ngOnInit(): void {
    this.route.paramMap
      .pipe(
        map((params) => toSafeMentorId(params.get('submissionId'))),
        distinctUntilChanged(),
        tap((submissionId) => this.resetForRoute(submissionId)),
        switchMap((submissionId) => {
          if (submissionId === null) return EMPTY;
          return this.retry$.pipe(
            startWith(undefined),
            tap(() => this.resetRequestState()),
            switchMap(() =>
              this.data.detail(submissionId).pipe(
                map((response): ME10LoadResult => ({ submissionId, response })),
                catchError((error: unknown) => of<ME10LoadResult>({ submissionId, error })),
              ),
            ),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyResult(result));
  }

  load(): void {
    if (this.submissionId()) this.retry$.next();
  }

  private resetForRoute(submissionId: string | null): void {
    this.submissionId.set(submissionId ?? '');
    this.submission.set(null);
    this.error.set(null);
    this.notFound.set(false);
    this.forbidden.set(false);
    this.invalidId.set(submissionId === null);
    this.loading.set(submissionId !== null);
  }

  private resetRequestState(): void {
    this.submission.set(null);
    this.error.set(null);
    this.notFound.set(false);
    this.forbidden.set(false);
    this.loading.set(true);
  }

  private applyResult(result: ME10LoadResult): void {
    if (this.submissionId() !== result.submissionId) return;
    this.loading.set(false);

    if ('error' in result) {
      this.notFound.set(hasHttpStatus(result.error, 404));
      this.forbidden.set(hasHttpStatus(result.error, 403));
      if (!this.notFound() && !this.forbidden()) this.error.set(mentorApiErrorMessage(result.error));
      return;
    }

    const envelope: unknown = result.response;
    if (!isApiEnvelope(envelope)) {
      this.error.set('Study Server trả về phản hồi không hợp lệ.');
      return;
    }
    if (!envelope.success) {
      this.notFound.set(envelope.businessCode === 'DESIGN_RESOURCE_NOT_FOUND');
      this.forbidden.set(envelope.businessCode === 'DESIGN_ACCESS_DENIED');
      if (!this.notFound() && !this.forbidden()) {
        this.error.set(envelope.message || 'Study Server không xác nhận yêu cầu.');
      }
      return;
    }
    if (
      envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isSubmission(envelope.data) ||
      toSafeMentorId(envelope.data.id) !== result.submissionId
    ) {
      this.error.set('Study Server trả về bài nộp không khớp với đường dẫn.');
      return;
    }

    this.submission.set(envelope.data);
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isApiEnvelope(value: unknown): value is ApiEnvelope<unknown> {
  return (
    isRecord(value) &&
    typeof value['success'] === 'boolean' &&
    typeof value['businessCode'] === 'string' &&
    typeof value['message'] === 'string' &&
    isRecord(value['meta']) &&
    typeof value['traceId'] === 'string'
  );
}

function isSubmission(value: unknown): value is MentorSubmission {
  if (
    !isRecord(value) ||
    toSafeMentorId(value['id']) === null ||
    toSafeMentorId(value['assignment_id']) === null ||
    toSafeMentorId(value['user_id']) === null ||
    typeof value['status'] !== 'string' ||
    typeof value['submitted_at'] !== 'string' ||
    Number.isNaN(Date.parse(value['submitted_at'])) ||
    !Array.isArray(value['files'])
  ) {
    return false;
  }
  if (value['content'] !== undefined && value['content'] !== null && typeof value['content'] !== 'string') return false;
  if (value['score'] !== undefined && value['score'] !== null && typeof value['score'] !== 'string') return false;
  if (value['feedback'] !== undefined && value['feedback'] !== null && typeof value['feedback'] !== 'string') return false;
  return value['files'].every(isUploadAsset);
}

function isUploadAsset(value: unknown): boolean {
  return (
    isRecord(value) &&
    toSafeMentorId(value['id']) !== null &&
    typeof value['name'] === 'string' &&
    typeof value['url'] === 'string' &&
    typeof value['content_type'] === 'string' &&
    Number.isSafeInteger(value['size_bytes']) && Number(value['size_bytes']) >= 0 &&
    typeof value['status'] === 'string'
  );
}

function hasHttpStatus(error: unknown, status: number): boolean {
  return isRecord(error) && error['status'] === status;
}
