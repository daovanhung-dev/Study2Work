import { HttpErrorResponse } from '@angular/common/http';
import { signal } from '@angular/core';
import { Observable } from 'rxjs';

import type { ApiEnvelope } from '../../../core/http/api-envelope';

export type StudentApiStatus = 'idle' | 'loading' | 'ready' | 'error';

export class StudentApiState<T> {
  readonly status = signal<StudentApiStatus>('idle');
  readonly data = signal<T | null>(null);
  readonly error = signal('');

  load(request: Observable<ApiEnvelope<T>>, onSuccess?: (data: T) => void): void {
    this.status.set('loading');
    this.data.set(null);
    this.error.set('');

    request.subscribe({
      next: (response) => {
        if (!response?.success) {
          this.status.set('error');
          this.error.set(response?.message || 'API không trả dữ liệu thành công.');
          return;
        }

        this.data.set(response.data);
        this.status.set('ready');
        onSuccess?.(response.data);
      },
      error: (error: unknown) => {
        this.status.set('error');
        this.error.set(getStudentApiErrorMessage(error));
      },
    });
  }

  clear(): void {
    this.data.set(null);
    this.error.set('');
    this.status.set('idle');
  }
}

export function getStudentApiErrorMessage(error: unknown): string {
  if (!(error instanceof HttpErrorResponse)) {
    return 'Không thể đọc dữ liệu từ API.';
  }

  if (error.status === 0) {
    return 'Không kết nối được Study Server. Hãy kiểm tra server hoặc thử lại sau.';
  }
  if (error.status === 401) {
    return 'Bạn cần đăng nhập để xem dữ liệu này.';
  }
  if (error.status === 403) {
    return 'Tài khoản hiện tại không có quyền truy cập nội dung này.';
  }
  if (error.status === 404) {
    return 'API chưa có trên Study Server hoặc không tìm thấy dữ liệu.';
  }

  const apiMessage = readApiMessage(error.error);
  return apiMessage || `Study Server trả về lỗi ${error.status}.`;
}

function readApiMessage(body: unknown): string | undefined {
  if (!body || typeof body !== 'object' || !('message' in body)) {
    return undefined;
  }

  const message = (body as { message?: unknown }).message;
  return typeof message === 'string' && message.trim() ? message : undefined;
}
