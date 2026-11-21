import { HttpErrorResponse } from '@angular/common/http';
import { Component, DestroyRef, OnInit, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Router, RouterLink } from '@angular/router';
import { finalize } from 'rxjs';

import { isOperationUuid } from '../../../shared/SH07/models/sh07-operation.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';
import { ME14NotificationCreateService } from '../data-access/me14-notification-create.service';

type NotificationChannel = 'PUSH' | 'EMAIL';

interface RecipientHandoff {
  id: string;
  full_name: string;
}

@Component({
  imports: [RouterLink, MentorPageHeader],
  selector: 'study-me14-page',
  styleUrls: ['./me14-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me14-page.html',
})
export class ME14Page implements OnInit {
  private readonly creator = inject(ME14NotificationCreateService);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);

  readonly courseId = signal('');
  readonly recipients = signal<RecipientHandoff[]>([]);
  readonly handoffError = signal<string | null>(null);
  readonly title = signal('');
  readonly content = signal('');
  readonly channels = signal<NotificationChannel[]>([]);
  readonly isSubmitting = signal(false);
  readonly submissionError = signal<string | null>(null);
  readonly submissionUncertain = signal(false);
  readonly acceptedOperationId = signal<string | null>(null);
  readonly titleCount = computed(() => this.title().length);
  readonly wordCount = computed(() => {
    const trimmed = this.content().trim();
    return trimmed ? trimmed.split(/\s+/).length : 0;
  });
  readonly canSubmit = computed(() =>
    !this.isSubmitting() &&
    !this.submissionUncertain() &&
    !this.acceptedOperationId() &&
    !this.handoffError() &&
    this.recipients().length > 0 &&
    !!this.title().trim() && this.title().length <= 200 &&
    !!this.content().trim() &&
    this.channels().length > 0,
  );

  ngOnInit(): void {
    const state: unknown = typeof history === 'undefined' ? null : history.state;
    if (!isRecord(state)) {
      this.handoffError.set('Chưa có dữ liệu người nhận. Hãy chọn người nhận từ ME-13.');
      return;
    }
    consumeRecipientHandoff(state);

    const courseId = toSafeMentorId(state['courseId']);
    const rawRecipients = state['recipients'];
    if (!courseId || !Array.isArray(rawRecipients)) {
      this.handoffError.set('Thông tin khóa học hoặc người nhận không hợp lệ. Hãy chọn lại ở ME-13.');
      return;
    }

    const recipients: RecipientHandoff[] = [];
    const ids = new Set<string>();
    for (const item of rawRecipients) {
      if (!isRecord(item)) {
        this.handoffError.set('Danh sách người nhận không hợp lệ. Hãy chọn lại ở ME-13.');
        return;
      }
      const id = toSafeMentorId(item['id']);
      const fullName = item['full_name'];
      if (!id || typeof fullName !== 'string' || ids.has(id)) {
        this.handoffError.set('Danh sách người nhận không hợp lệ hoặc có ID trùng. Hãy chọn lại ở ME-13.');
        return;
      }
      ids.add(id);
      recipients.push({ id, full_name: fullName });
    }

    if (!recipients.length) {
      this.handoffError.set('Chưa có người nhận. Hãy chọn ít nhất một học viên ở ME-13.');
      return;
    }

    this.courseId.set(courseId);
    this.recipients.set(recipients);
  }

  toggleChannel(channel: NotificationChannel, checked: boolean): void {
    if (this.acceptedOperationId() || this.submissionUncertain()) return;
    this.channels.update((current) => checked
      ? current.includes(channel) ? current : [...current, channel]
      : current.filter((item) => item !== channel));
  }

  updateTitle(value: string): void {
    if (this.acceptedOperationId() || this.submissionUncertain()) return;
    this.title.set(value);
  }

  updateContent(value: string): void {
    if (this.acceptedOperationId() || this.submissionUncertain()) return;
    this.content.set(value);
  }

  submitNotification(event: SubmitEvent): void {
    event.preventDefault();
    if (!this.canSubmit()) return;

    const recipientIds = this.recipients().map((recipient) => recipient.id).join(',');
    const channels = this.channels().join(',');
    this.submissionError.set(null);
    this.isSubmitting.set(true);

    this.creator
      .create(recipientIds, this.title().trim(), this.content().trim(), channels)
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        finalize(() => this.isSubmitting.set(false)),
      )
      .subscribe({
        next: (envelope) => {
          const operationId = readAcceptedOperationId(envelope);
          if (!operationId) {
            this.submissionUncertain.set(true);
            this.submissionError.set('Study Server chưa xác nhận yêu cầu. Hãy kiểm tra lại trước khi gửi lần nữa.');
            return;
          }
          this.acceptedOperationId.set(operationId);
          void this.router.navigateByUrl(`/operations/${operationId}`, {
            state: { sh07ReturnTo: '/mentor/notifications/new' },
          });
        },
        error: (error: unknown) => {
          this.submissionError.set(presentCreateError(error));
          this.submissionUncertain.set(isAmbiguousCreateFailure(error));
        },
      });
  }
}

function isAmbiguousCreateFailure(error: unknown): boolean {
  // API #63 has no idempotency key. A lost/malformed response can mean the
  // batch was committed, so the client must not blindly create it again.
  return !(error instanceof HttpErrorResponse) || error.status === 0;
}

function consumeRecipientHandoff(state: Record<string, unknown>): void {
  if (typeof history === 'undefined' || typeof location === 'undefined') return;
  const remainingState = { ...state };
  delete remainingState['courseId'];
  delete remainingState['recipients'];
  // Keep Angular's navigation metadata but remove recipient identifiers from
  // the current history entry so reload/back cannot replay the same handoff.
  history.replaceState(remainingState, '', location.href);
}

function readAcceptedOperationId(value: unknown): string | null {
  if (!isRecord(value) || value['success'] !== true || value['businessCode'] !== 'DESIGN_OPERATION_ACCEPTED') {
    return null;
  }
  const data = value['data'];
  if (!isRecord(data) || data['kind'] !== 'NOTIFICATION_DISPATCH' || data['status'] !== 'QUEUED') {
    return null;
  }
  return isOperationUuid(data['id']) ? data['id'] : null;
}

function presentCreateError(error: unknown): string {
  if (error instanceof HttpErrorResponse) {
    if (error.status === 401) return 'Phiên đăng nhập không còn hợp lệ. Hãy đăng nhập lại.';
    if (error.status === 403) return 'Một hoặc nhiều người nhận không nằm trong danh sách học viên bạn được phép gửi.';
    if (error.status === 422) return 'Kiểm tra lại tiêu đề, nội dung, người nhận và kênh gửi.';
    if (error.status === 503) return 'Dịch vụ đang tạm thời không khả dụng. Yêu cầu chưa được xác nhận.';
    if (error.status === 0) return 'Không thể kết nối tới Study Server. Yêu cầu chưa được xác nhận.';
  }
  return 'Không thể xác nhận yêu cầu gửi thông báo. Hãy thử lại sau.';
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}
