import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { Me12ThreadService } from '../data-access/me12-thread.service';
import {
  type SupportRequestDetailDto,
  type ThreadActionStatus,
  parseSupportRequestId,
} from '../models/me12-thread.models';
import { Me12ComposerResolve } from '../ui/me12-composer-resolve';
import { Me12ThreadPanel } from '../ui/me12-thread-panel';

export type Me12ScreenState =
  | 'invalid-param'
  | 'loading'
  | 'ready'
  | 'unauthorized'
  | 'forbidden'
  | 'not-found'
  | 'error';

@Component({
  imports: [RouterLink, Me12ThreadPanel, Me12ComposerResolve],
  selector: 'study-me12-page',
  styleUrl: './me12-page.css',
  templateUrl: './me12-page.html',
})
export class ME12Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly threadService = inject(Me12ThreadService);

  readonly requestId = signal<number | null>(null);
  readonly screenState = signal<Me12ScreenState>('loading');
  readonly errorMessage = signal<string>('');
  readonly traceId = signal<string>('');

  readonly requestDetail = signal<SupportRequestDetailDto | null>(null);
  readonly refreshingThread = signal<boolean>(false);

  readonly replyDraft = signal<string>('');
  readonly replyStatus = signal<ThreadActionStatus>('idle');
  readonly replyMessage = signal<string>('');

  readonly confirmResolvedChecked = signal<boolean>(false);
  readonly resolveStatus = signal<ThreadActionStatus>('idle');
  readonly resolveMessage = signal<string>('');

  ngOnInit(): void {
    const rawId = this.route.snapshot.paramMap.get('requestId');
    const parsed = parseSupportRequestId(rawId);
    if (parsed === null) {
      this.requestId.set(null);
      this.screenState.set('invalid-param');
      this.errorMessage.set('Mã yêu cầu hỗ trợ trên đường dẫn không phải số nguyên dương int64 hợp lệ.');
      return;
    }

    this.requestId.set(parsed);
    this.loadThread(parsed, true);
  }

  onReplyDraftChange(value: string): void {
    this.replyDraft.set(value);
    if (this.replyStatus() !== 'idle') {
      this.replyStatus.set('idle');
      this.replyMessage.set('');
    }
  }

  onConfirmResolveChange(checked: boolean): void {
    this.confirmResolvedChecked.set(checked);
  }

  refreshThread(): void {
    const id = this.requestId();
    if (id !== null) {
      this.loadThread(id, false);
    }
  }

  submitReply(): void {
    const id = this.requestId();
    const message = this.replyDraft();
    if (id === null || this.replyStatus() === 'saving') {
      return;
    }
    if (message.trim().length === 0) {
      this.replyStatus.set('error');
      this.replyMessage.set('Nội dung phản hồi không được để trống hoặc chỉ chứa khoảng trắng.');
      return;
    }

    this.replyStatus.set('saving');
    this.replyMessage.set('');

    this.threadService
      .sendReply(id, {
        message,
        attachment_refs: '[]',
      })
      .subscribe({
        next: (envelope) => {
          if (envelope.data) {
            this.requestDetail.set(envelope.data);
          }
          this.replyDraft.set('');
          this.replyStatus.set('saved');
          this.replyMessage.set('Đã gửi câu trả lời thành công qua API #60.');
          this.loadThread(id, false);
        },
        error: (err: unknown) => {
          this.replyStatus.set('error');
          this.replyMessage.set(
            this.extractErrorMessage(err, 'Không thể gửi câu trả lời qua API #60.'),
          );
        },
      });
  }

  submitResolve(): void {
    const id = this.requestId();
    if (id === null || !this.confirmResolvedChecked() || this.resolveStatus() === 'saving') {
      return;
    }

    this.resolveStatus.set('saving');
    this.resolveMessage.set('');

    this.threadService.resolveRequest(id).subscribe({
      next: (envelope) => {
        if (envelope.data) {
          this.requestDetail.set(envelope.data);
        }
        this.resolveStatus.set('saved');
        this.resolveMessage.set('Yêu cầu hỗ trợ đã được chuyển sang trạng thái RESOLVED (API #61).');
      },
      error: (err: unknown) => {
        this.resolveStatus.set('error');
        this.resolveMessage.set(
          this.extractErrorMessage(err, 'Không thể đóng yêu cầu hỗ trợ qua API #61.'),
        );
      },
    });
  }

  backToInbox(): void {
    void this.router.navigate(['/mentor/support']);
  }

  private loadThread(requestId: number, initial: boolean): void {
    if (initial) {
      this.screenState.set('loading');
    } else {
      this.refreshingThread.set(true);
    }
    this.errorMessage.set('');
    this.traceId.set('');

    this.threadService.getSupportRequestDetail(requestId).subscribe({
      next: (envelope) => {
        this.refreshingThread.set(false);
        this.requestDetail.set(envelope.data);
        this.traceId.set(envelope.traceId ?? '');
        this.screenState.set('ready');
      },
      error: (err: unknown) => {
        this.refreshingThread.set(false);
        if (!initial && this.requestDetail() !== null) {
          return;
        }
        this.handleLoadError(err);
      },
    });
  }

  private handleLoadError(err: unknown): void {
    if (err instanceof HttpErrorResponse) {
      const body = err.error as { message?: string; traceId?: string } | null;
      this.traceId.set(body?.traceId ?? '');
      if (err.status === 401) {
        this.screenState.set('unauthorized');
        this.errorMessage.set('Phiên đăng nhập giảng viên chưa xác thực hoặc đã hết hạn (401).');
        return;
      }
      if (err.status === 403) {
        this.screenState.set('forbidden');
        this.errorMessage.set('Bạn không có quyền truy cập yêu cầu hỗ trợ này (403).');
        return;
      }
      if (err.status === 404) {
        this.screenState.set('not-found');
        this.errorMessage.set('Không tìm thấy yêu cầu hỗ trợ theo mã đã cung cấp (404).');
        return;
      }
      this.errorMessage.set(body?.message ?? 'Không thể tải chi tiết yêu cầu hỗ trợ.');
    } else {
      this.errorMessage.set('Lỗi kết nối tới máy chủ Study API.');
    }
    this.screenState.set('error');
  }

  private extractErrorMessage(err: unknown, fallback: string): string {
    if (err instanceof HttpErrorResponse) {
      const body = err.error as { message?: string } | null;
      if (body?.message) {
        return body.message;
      }
    }
    return fallback;
  }
}
