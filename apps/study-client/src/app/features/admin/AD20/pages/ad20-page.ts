import { HttpErrorResponse } from '@angular/common/http';
import type { HttpResponse } from '@angular/common/http';
import { Component, DestroyRef, OnInit, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Router, RouterLink } from '@angular/router';
import { finalize } from 'rxjs';

import { AdminSessionError } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { isOperationUuid } from '../../../shared/SH07/models/sh07-operation.models';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD20_SCREEN } from '../models/ad20-screen.model';
import {
  AD20NotificationService,
  type AD20NotificationAcceptedData,
} from '../data-access/ad20-notification.service';

type NotificationChannel = 'PUSH' | 'EMAIL';

interface RecipientOption {
  readonly id: number | null;
  readonly full_name: string;
  readonly email: string;
  readonly role: string;
  readonly status: string;
}

interface RecipientPagination {
  readonly page: number;
  readonly size: number;
  readonly total: number;
  readonly total_pages: number;
}

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad20-page',
  templateUrl: './ad20-page.html',
})
export class AD20Page implements OnInit {
  private readonly notifications = inject(AD20NotificationService);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);

  readonly definition = AD20_SCREEN;
  readonly title = signal('');
  readonly content = signal('');
  readonly channels = signal<NotificationChannel[]>([]);
  readonly recipients = signal<readonly RecipientOption[]>([]);
  readonly selectedRecipients = signal<readonly RecipientOption[]>([]);
  readonly pagination = signal<RecipientPagination | null>(null);
  readonly recipientsLoading = signal(false);
  readonly recipientsError = signal<string | null>(null);
  readonly isSubmitting = signal(false);
  readonly submissionError = signal<string | null>(null);
  readonly acceptedOperationId = signal<string | null>(null);
  readonly submissionUnconfirmed = signal(false);

  readonly previewTitle = computed(() => this.title().trim() || 'Chưa nhập tiêu đề');
  readonly previewContent = computed(() => this.content().trim() || 'Nội dung xem trước sẽ hiển thị tại đây.');
  readonly selectedRecipientCount = computed(() => this.selectedRecipients().length);
  readonly canSubmit = computed(() =>
    !this.isSubmitting() &&
    !this.acceptedOperationId() &&
    !this.submissionUnconfirmed() &&
    this.selectedRecipients().length > 0 &&
    !!this.title().trim() && this.title().length <= 200 &&
    !!this.content().trim() &&
    this.channels().length > 0,
  );
  readonly isFormLocked = computed(() =>
    !!this.acceptedOperationId() || this.submissionUnconfirmed(),
  );

  ngOnInit(): void {
    this.loadRecipients(1);
  }

  updateTitle(event: Event): void {
    if (!this.isFormLocked() && event.target instanceof HTMLInputElement) {
      this.submissionError.set(null);
      this.title.set(event.target.value);
    }
  }

  updateContent(event: Event): void {
    if (!this.isFormLocked() && event.target instanceof HTMLTextAreaElement) {
      this.submissionError.set(null);
      this.content.set(event.target.value);
    }
  }

  toggleChannel(channel: NotificationChannel, checked: boolean): void {
    if (this.isFormLocked()) return;
    this.submissionError.set(null);
    this.channels.update((current) => checked
      ? current.includes(channel) ? current : [...current, channel]
      : current.filter((item) => item !== channel));
  }

  isSelected(id: number | null): boolean {
    return id !== null && this.selectedRecipients().some((recipient) => recipient.id === id);
  }

  toggleRecipient(recipient: RecipientOption, checked: boolean): void {
    if (recipient.id === null || this.isFormLocked()) return;
    this.submissionError.set(null);
    this.selectedRecipients.update((current) => checked
      ? current.some((item) => item.id === recipient.id) ? current : [...current, recipient]
      : current.filter((item) => item.id !== recipient.id));
  }

  removeRecipient(recipientId: number | null): void {
    if (recipientId === null || this.isFormLocked()) return;
    this.submissionError.set(null);
    this.selectedRecipients.update((current) => current.filter((recipient) => recipient.id !== recipientId));
  }

  loadRecipients(page: number): void {
    if (this.recipientsLoading() || this.isFormLocked()) return;
    this.recipientsLoading.set(true);
    this.recipientsError.set(null);

    this.notifications
      .getRecipients(page)
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        finalize(() => this.recipientsLoading.set(false)),
      )
      .subscribe({
        next: (envelope) => {
          if (!isRecipientEnvelope(envelope)) {
            this.recipientsError.set('Danh sách người dùng chưa có định dạng hợp lệ. Hãy thử tải lại.');
            return;
          }
          const parsed = parseRecipientPage(envelope.data, page);
          if (!parsed) {
            this.recipientsError.set('Danh sách người dùng chưa có định dạng hợp lệ. Hãy thử tải lại.');
            return;
          }
          this.recipients.set(parsed.items);
          this.pagination.set(parsed.pagination);
        },
        error: (error: unknown) => this.recipientsError.set(presentRecipientsError(error)),
      });
  }

  submitNotification(event: SubmitEvent): void {
    event.preventDefault();
    if (!this.canSubmit()) return;
    const recipientIds = this.selectedRecipients()
      .map((recipient) => recipient.id)
      .filter((id): id is number => id !== null);
    if (recipientIds.length !== this.selectedRecipients().length) {
      this.submissionError.set('Một người nhận có ID không thể gửi an toàn. Hãy bỏ chọn và chọn lại.');
      return;
    }

    this.submissionError.set(null);
    this.isSubmitting.set(true);
    this.notifications
      .createNotification({
        recipients: recipientIds,
        title: this.title().trim(),
        content: this.content().trim(),
        channels: this.channels(),
      })
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        finalize(() => this.isSubmitting.set(false)),
      )
      .subscribe({
        next: (envelope) => {
          const operationId = readAcceptedOperationId(envelope);
          if (!operationId) {
            this.submissionUnconfirmed.set(true);
            this.submissionError.set('Phản hồi chưa xác nhận được mã theo dõi. Không gửi lại yêu cầu này; hãy kiểm tra danh sách thông báo trước.');
            return;
          }
          this.acceptedOperationId.set(operationId);
          void this.router.navigateByUrl(`/operations/${operationId}`, {
            state: { sh07ReturnTo: '/admin/notifications/new' },
          });
        },
        error: (error: unknown) => {
          if (isAmbiguousCreateOutcome(error)) {
            this.submissionUnconfirmed.set(true);
            this.submissionError.set('Chưa xác định được máy chủ đã tiếp nhận yêu cầu hay chưa. Không gửi lại; hãy kiểm tra danh sách thông báo trước.');
            return;
          }
          this.submissionError.set(presentCreateError(error));
        },
      });
  }
}

function isAmbiguousCreateOutcome(error: unknown): boolean {
  if (error instanceof AdminSessionError) return false;
  if (!(error instanceof HttpErrorResponse)) return true;
  return error.status === 0 || error.status >= 500;
}

function isRecipientEnvelope(value: unknown): value is { success: boolean; businessCode: string; data: unknown } {
  if (!isRecord(value)) return false;
  return value['success'] === true &&
    value['businessCode'] === 'DESIGN_RESOURCE_RETRIEVED' &&
    typeof value['message'] === 'string' &&
    isRecord(value['meta']) &&
    typeof value['traceId'] === 'string';
}

function parseRecipientPage(value: unknown, requestedPage: number): {
  items: RecipientOption[];
  pagination: RecipientPagination;
} | null {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) return null;
  const pagination = value['pagination'];
  const page = pagination['page'];
  const size = pagination['size'];
  const total = pagination['total'];
  const totalPages = pagination['total_pages'];
  if (
    !isPositiveSafeInteger(page) || page !== requestedPage ||
    !isPositiveSafeInteger(size) || !isNonnegativeSafeInteger(total) ||
    !isNonnegativeSafeInteger(totalPages)
  ) return null;

  const items: RecipientOption[] = [];
  for (const raw of value['items']) {
    if (!isRecord(raw)) return null;
    const fullName = raw['full_name'];
    const email = raw['email'];
    const role = raw['role'];
    const status = raw['status'];
    if (
      (typeof raw['id'] !== 'number' || !Number.isInteger(raw['id']) || raw['id'] < 1) ||
      typeof fullName !== 'string' || typeof email !== 'string' ||
      typeof role !== 'string' || typeof status !== 'string'
    ) return null;
    items.push({
      id: Number.isSafeInteger(raw['id']) ? raw['id'] : null,
      full_name: fullName,
      email,
      role,
      status,
    });
  }
  return {
    items,
    pagination: { page, size, total, total_pages: totalPages },
  };
}

function readAcceptedOperationId(
  response: HttpResponse<ApiEnvelope<AD20NotificationAcceptedData>>,
): string | null {
  if (response.status !== 202) return null;
  const envelope = response.body;
  if (!envelope || envelope.success !== true || envelope.businessCode !== 'DESIGN_OPERATION_ACCEPTED') {
    return null;
  }
  const data = envelope.data;
  const meta = envelope.meta;
  if (!isRecord(data) || data['status'] !== 'QUEUED' || !isRecord(meta)) return null;
  return isOperationUuid(meta['operation_id']) ? meta['operation_id'] : null;
}

function presentRecipientsError(error: unknown): string {
  if (error instanceof HttpErrorResponse) {
    if (error.status === 401) return 'Phiên đăng nhập không còn hợp lệ. Hãy đăng nhập lại.';
    if (error.status === 403) return 'Tài khoản hiện tại không có quyền xem danh sách người nhận.';
    if (error.status === 0) return 'Không thể kết nối tới Study Server. Hãy thử tải danh sách lại.';
  }
  return 'Không thể tải danh sách người nhận. Hãy thử lại sau.';
}

function presentCreateError(error: unknown): string {
  if (error instanceof HttpErrorResponse) {
    if (error.status === 401) return 'Phiên đăng nhập không còn hợp lệ. Hãy đăng nhập lại.';
    if (error.status === 403) return 'Tài khoản hiện tại không có quyền tạo thông báo.';
    if (error.status === 422) return 'Kiểm tra lại người nhận, tiêu đề, nội dung và kênh gửi.';
    if (error.status === 503) return 'Dịch vụ đang tạm thời không khả dụng. Yêu cầu chưa được xác nhận.';
    if (error.status === 0) return 'Không thể kết nối tới Study Server. Yêu cầu chưa được xác nhận.';
  }
  return 'Không thể xác nhận yêu cầu gửi thông báo. Hãy thử lại sau.';
}

function isPositiveSafeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isSafeInteger(value) && value > 0;
}

function isNonnegativeSafeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isSafeInteger(value) && value >= 0;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}
