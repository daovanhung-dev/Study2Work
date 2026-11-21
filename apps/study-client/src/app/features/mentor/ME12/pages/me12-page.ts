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

import { ME12SupportThreadService } from '../data-access/me12-support-thread.service';
import type { MentorSupportRequest } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

type ME12ReadResult =
  | { requestId: string; response: ApiEnvelope<MentorSupportRequest> }
  | { requestId: string; error: unknown };

@Component({
  imports: [DatePipe, RouterLink, MentorPageHeader],
  selector: 'study-me12-page',
  styleUrls: ['./me12-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me12-page.html',
})
export class ME12Page implements OnInit {
  private readonly data = inject(ME12SupportThreadService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly route = inject(ActivatedRoute);
  private readonly retry$ = new Subject<void>();
  private uncertainReplyMessageIds = new Set<string>();
  private uncertainReplyText: string | null = null;

  readonly requestId = signal('');
  readonly request = signal<MentorSupportRequest | null>(null);
  readonly loading = signal(true);
  readonly sending = signal(false);
  readonly error = signal<string | null>(null);
  readonly actionError = signal<string | null>(null);
  readonly actionSuccess = signal<string | null>(null);
  readonly invalidId = signal(false);
  readonly notFound = signal(false);
  readonly forbidden = signal(false);
  readonly replyUncertain = signal(false);
  readonly replyDraft = signal('');

  ngOnInit(): void {
    this.route.paramMap
      .pipe(
        map((params) => toSafeMentorId(params.get('requestId'))),
        distinctUntilChanged(),
        tap((requestId) => this.resetForRoute(requestId)),
        switchMap((requestId) => {
          if (requestId === null) return EMPTY;
          return this.retry$.pipe(
            startWith(undefined),
            tap(() => this.resetReadState()),
            switchMap(() =>
              this.data.detail(requestId).pipe(
                map((response): ME12ReadResult => ({ requestId, response })),
                catchError((error: unknown) => of<ME12ReadResult>({ requestId, error })),
              ),
            ),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyReadResult(result));
  }

  load(): void {
    if (this.requestId()) this.retry$.next();
  }

  reply(event: SubmitEvent, message: string): void {
    event.preventDefault();
    const requestId = this.requestId();
    if (
      !requestId ||
      !this.canReply() ||
      this.sending() ||
      this.replyUncertain() ||
      this.loading()
    ) return;
    if (!message.trim()) {
      this.actionError.set('Câu trả lời không được để trống.');
      return;
    }

    const before = this.request();
    this.sending.set(true);
    this.actionError.set(null);
    this.actionSuccess.set(null);
    this.data.reply(requestId, message).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (response) => {
        if (this.requestId() !== requestId) return;
        this.sending.set(false);
        const envelope: unknown = response;
        if (!isApiEnvelope(envelope)) {
          this.markReplyUncertain('Phản hồi gửi không hợp lệ.', message);
          return;
        }
        if (!envelope.success) {
          this.actionError.set(envelope.message || 'Study Server không xác nhận câu trả lời.');
          return;
        }
        if (
          envelope.businessCode !== 'DESIGN_RESOURCE_UPDATED' ||
          !isSupportRequest(envelope.data) ||
          toSafeMentorId(envelope.data.id) !== requestId ||
          !containsNewReply(before, envelope.data, message)
        ) {
          this.markReplyUncertain('Chưa xác nhận được câu trả lời trong thread.', message);
          return;
        }
        this.request.set(envelope.data);
        this.replyUncertain.set(false);
        this.replyDraft.set('');
        this.uncertainReplyMessageIds.clear();
        this.uncertainReplyText = null;
        this.actionSuccess.set('Câu trả lời đã được Study Server ghi nhận.');
        this.load();
      },
      error: (error: unknown) => {
        if (this.requestId() !== requestId) return;
        this.sending.set(false);
        this.markReplyUncertain(mentorApiErrorMessage(error), message);
      },
    });
  }

  canReply(): boolean {
    return ['OPEN', 'IN_PROGRESS', 'WAITING_LEARNER'].includes(this.request()?.status ?? '');
  }

  isResolveCandidate(status: string): boolean {
    return ['OPEN', 'IN_PROGRESS', 'WAITING_LEARNER'].includes(status);
  }

  private resetForRoute(requestId: string | null): void {
    this.requestId.set(requestId ?? '');
    this.request.set(null);
    this.error.set(null);
    this.actionError.set(null);
    this.actionSuccess.set(null);
    this.notFound.set(false);
    this.forbidden.set(false);
    this.invalidId.set(requestId === null);
    this.replyUncertain.set(false);
    this.replyDraft.set('');
    this.uncertainReplyMessageIds.clear();
    this.uncertainReplyText = null;
    this.sending.set(false);
    this.loading.set(requestId !== null);
  }

  private resetReadState(): void {
    this.request.set(null);
    this.error.set(null);
    this.notFound.set(false);
    this.forbidden.set(false);
    this.loading.set(true);
  }

  private applyReadResult(result: ME12ReadResult): void {
    if (this.requestId() !== result.requestId) return;
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
      if (!this.notFound() && !this.forbidden()) this.error.set(envelope.message || 'Study Server không xác nhận yêu cầu.');
      return;
    }
    if (
      envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isSupportRequest(envelope.data) ||
      toSafeMentorId(envelope.data.id) !== result.requestId
    ) {
      this.error.set('Study Server trả về thread không khớp với đường dẫn.');
      return;
    }
    this.request.set(envelope.data);
    if (this.replyUncertain()) {
      const uncertainText = this.uncertainReplyText;
      const appeared = uncertainText !== null && envelope.data.messages.some((message) => {
        const id = toSafeMentorId(message.id);
        return id !== null && !this.uncertainReplyMessageIds.has(id) && message.content === uncertainText;
      });
      this.actionError.set(null);
      if (appeared) {
        this.replyDraft.set('');
        this.actionSuccess.set('Câu trả lời đã xuất hiện trong thread sau khi tải lại.');
      } else {
        this.actionError.set('Thread đã được tải lại nhưng chưa xác nhận được câu trả lời trước đó. Kiểm tra nội dung rồi mới thử gửi lại.');
      }
      this.uncertainReplyMessageIds.clear();
      this.uncertainReplyText = null;
    }
    this.replyUncertain.set(false);
  }

  private markReplyUncertain(message: string, submittedText: string): void {
    this.uncertainReplyMessageIds = new Set(
      (this.request()?.messages ?? [])
        .map((item) => toSafeMentorId(item.id))
        .filter((id): id is string => id !== null),
    );
    this.uncertainReplyText = submittedText;
    this.replyUncertain.set(true);
    this.actionError.set(`${message} Không gửi lặp lại khi chưa tải lại thread.`);
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

function isSupportRequest(value: unknown): value is MentorSupportRequest {
  if (
    !isRecord(value) ||
    toSafeMentorId(value['id']) === null ||
    toSafeMentorId(value['course_id']) === null ||
    typeof value['status'] !== 'string' ||
    !isUserSummary(value['student']) ||
    !Array.isArray(value['messages']) ||
    !isDateTime(value['created_at']) ||
    (value['resolved_at'] !== undefined && value['resolved_at'] !== null && !isDateTime(value['resolved_at']))
  ) {
    return false;
  }
  const messageIds = new Set<string>();
  for (const message of value['messages']) {
    if (!isSupportMessage(message)) return false;
    const id = toSafeMentorId(message['id']);
    if (id === null || messageIds.has(id)) return false;
    messageIds.add(id);
  }
  return true;
}

function isSupportMessage(value: unknown): value is MentorSupportRequest['messages'][number] {
  return (
    isRecord(value) &&
    toSafeMentorId(value['id']) !== null &&
    isUserSummary(value['author']) &&
    typeof value['content'] === 'string' &&
    isDateTime(value['created_at']) &&
    Array.isArray(value['attachments']) &&
    value['attachments'].every(isUploadAsset)
  );
}

function isUserSummary(value: unknown): value is MentorSupportRequest['student'] {
  return (
    isRecord(value) &&
    toSafeMentorId(value['id']) !== null &&
    typeof value['full_name'] === 'string' &&
    (value['avatar_url'] === undefined || value['avatar_url'] === null || typeof value['avatar_url'] === 'string')
  );
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

function isDateTime(value: unknown): value is string {
  return typeof value === 'string' && !Number.isNaN(Date.parse(value));
}

function containsNewReply(
  previous: MentorSupportRequest | null,
  updated: MentorSupportRequest,
  message: string,
): boolean {
  const previousIds = new Set((previous?.messages ?? []).map((item) => toSafeMentorId(item.id)));
  return updated.messages.some((item) => {
    const id = toSafeMentorId(item.id);
    return id !== null && !previousIds.has(id) && item.content === message;
  });
}

function hasHttpStatus(error: unknown, status: number): boolean {
  return isRecord(error) && error['status'] === status;
}
