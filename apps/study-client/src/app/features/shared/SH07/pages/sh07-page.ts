import { HttpErrorResponse } from '@angular/common/http';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { finalize } from 'rxjs';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import {
  SH07AuthenticationRequiredError,
  SH07OperationService,
} from '../data-access/sh07-operation.service';
import { isOperationUuid, parseSH07Operation, type SH07NotificationOperation } from '../models/sh07-operation.models';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-sh07-page',
  styleUrl: './sh07-page.css',
  templateUrl: './sh07-page.html',
})
export class SH07Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly operationService = inject(SH07OperationService);
  private readonly destroyRef = inject(DestroyRef);

  readonly operationId = signal('');
  readonly operation = signal<SH07NotificationOperation | null>(null);
  readonly isLoading = signal(false);
  readonly errorMessage = signal<string | null>(null);
  readonly lastUpdated = signal<string | null>(null);
  readonly returnTo = signal('/');

  ngOnInit(): void {
    const routeState = typeof window === 'undefined' ? null : window.history.state;
    this.returnTo.set(safeInternalRoute(routeState?.['sh07ReturnTo']));
    this.operationId.set(this.route.snapshot.paramMap.get('operationId') ?? '');
    this.refresh();
  }

  refresh(): void {
    const operationId = this.operationId();
    this.errorMessage.set(null);
    if (!isOperationUuid(operationId)) {
      this.errorMessage.set('Mã tác vụ không hợp lệ hoặc không còn khả dụng.');
      return;
    }
    if (this.isLoading()) return;

    this.isLoading.set(true);
    this.operationService
      .getOperation(operationId)
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        finalize(() => this.isLoading.set(false)),
      )
      .subscribe({
        next: (envelope) => {
          if (!isOperationEnvelope(envelope)) {
            this.errorMessage.set('Hệ thống chưa trả về trạng thái tác vụ hợp lệ. Hãy thử tải lại.');
            return;
          }
          const operation = parseSH07Operation(envelope.data, operationId);
          if (!operation) {
            this.errorMessage.set('Hệ thống chưa trả về trạng thái tác vụ hợp lệ. Hãy thử tải lại.');
            return;
          }
          this.operation.set(operation);
          this.lastUpdated.set(new Date().toISOString());
        },
        error: (error: unknown) => this.errorMessage.set(presentOperationError(error)),
      });
  }

  statusLabel(status: SH07NotificationOperation['status']): string {
    switch (status) {
      case 'QUEUED': return 'Đã tiếp nhận · đang chờ xử lý';
      case 'FAILED': return 'Không thể hoàn tất';
      case 'SENT': return 'Đã hoàn tất';
    }
  }

  formatTimestamp(value: string): string {
    return new Intl.DateTimeFormat('vi-VN', { dateStyle: 'medium', timeStyle: 'short' })
      .format(new Date(value));
  }
}

function isOperationEnvelope(value: unknown): value is ApiEnvelope<unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return false;
  const envelope = value as Record<string, unknown>;
  return envelope['success'] === true &&
    envelope['businessCode'] === 'DESIGN_OPERATION_RETRIEVED' &&
    typeof envelope['message'] === 'string' &&
    typeof envelope['traceId'] === 'string';
}

function presentOperationError(error: unknown): string {
  if (error instanceof SH07AuthenticationRequiredError) {
    return 'Đăng nhập bằng tài khoản đã gửi tác vụ để xem trạng thái này.';
  }
  if (error instanceof HttpErrorResponse) {
    if (error.status === 401) return 'Phiên đăng nhập không còn hợp lệ. Hãy đăng nhập lại để tiếp tục.';
    if (error.status === 403) return 'Tài khoản hiện tại không có quyền xem trạng thái tác vụ này.';
    if (error.status === 404) return 'Không tìm thấy tác vụ hoặc tác vụ không thuộc tài khoản hiện tại.';
    if (error.status === 0) return 'Không thể kết nối tới Study Server. Hãy thử tải lại.';
  }
  return 'Không thể tải trạng thái tác vụ. Hãy thử lại sau.';
}

function safeInternalRoute(value: unknown): string {
  if (
    typeof value !== 'string' ||
    !value.startsWith('/') ||
    value.startsWith('//') ||
    value.includes('\\') ||
    /[\u0000-\u001f]/.test(value)
  ) {
    return '/';
  }
  return value;
}
