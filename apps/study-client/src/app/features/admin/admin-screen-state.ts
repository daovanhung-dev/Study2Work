import { HttpErrorResponse } from '@angular/common/http';
import type { ActivatedRoute } from '@angular/router';
import { toObservable, toSignal } from '@angular/core/rxjs-interop';
import type { Signal } from '@angular/core';
import { catchError, map, of, startWith, switchMap } from 'rxjs';
import type { Observable } from 'rxjs';

import { AdminSessionError } from '../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../core/http/api-envelope';
import type {
  AdminScreenField,
  AdminScreenMetric,
  AdminScreenRow,
  AdminScreenSection,
  AdminScreenViewState,
} from '../../shared/ui/admin-screen.model';

export const ADMIN_LOADING_STATE: AdminScreenViewState = { status: 'loading' };

export function adminQueryState<TQuery, TResponse>(
  query: Signal<TQuery>,
  load: (query: TQuery) => Observable<ApiEnvelope<TResponse>>,
  render: (response: TResponse) => AdminScreenViewState,
  successBusinessCode?: string,
): Signal<AdminScreenViewState> {
  return toSignal(
    toObservable(query).pipe(
      switchMap((value) =>
        load(value).pipe(
          map((envelope): AdminScreenViewState =>
            envelope.success === true
              && (successBusinessCode === undefined || envelope.businessCode === successBusinessCode)
              ? render(envelope.data)
              : { status: 'error', message: 'Study Server không thể tải dữ liệu lúc này.' },
          ),
          startWith(ADMIN_LOADING_STATE),
          catchError((error: unknown) => of(adminDataError(error))),
        ),
      ),
    ),
    { initialValue: ADMIN_LOADING_STATE },
  );
}

export function adminRouteState<TResponse>(
  route: ActivatedRoute,
  parameter: string,
  load: (id: string) => Observable<ApiEnvelope<TResponse>>,
  render: (response: TResponse) => AdminScreenViewState,
  validateId?: (id: string) => boolean,
  invalidIdMessage = 'Mã tham chiếu trên đường dẫn không hợp lệ.',
  successBusinessCode?: string,
): Signal<AdminScreenViewState> {
  return toSignal(
    route.paramMap.pipe(
      switchMap((params) => {
        const id = params.get(parameter);
        if (!id) {
          return of<AdminScreenViewState>({
            status: 'error',
            message: 'Thiếu mã tham chiếu trên đường dẫn.',
          });
        }
        if (validateId && !validateId(id)) {
          return of<AdminScreenViewState>({ status: 'error', message: invalidIdMessage });
        }
        return load(id).pipe(
          map((envelope): AdminScreenViewState => {
            const hasExpectedSuccess = envelope.success === true
              && (successBusinessCode === undefined || envelope.businessCode === successBusinessCode);
            return hasExpectedSuccess
              ? render(envelope.data)
              : { status: 'error', message: 'Study Server không thể tải dữ liệu lúc này.' };
          }),
          startWith(ADMIN_LOADING_STATE),
          catchError((error: unknown) => of(adminDataError(error))),
        );
      }),
    ),
    { initialValue: ADMIN_LOADING_STATE },
  );
}

export function isSignedInt64RouteId(value: string): boolean {
  const match = /^[+-]?[0-9]+$/.exec(value);
  if (value.length > 20 || match?.[0] !== value) {
    return false;
  }

  const negative = value.startsWith('-');
  const digits = value.replace(/^[+-]/, '').replace(/^0+/, '') || '0';
  const maxMagnitude = negative ? '9223372036854775808' : '9223372036854775807';
  return digits.length < maxMagnitude.length
    || (digits.length === maxMagnitude.length && digits <= maxMagnitude);
}

export function loadedRows(
  rows: readonly AdminScreenRow[],
  pagination?: { page: number; total: number; totalPages: number; size?: number },
): AdminScreenViewState {
  return { status: 'loaded', rows, pagination };
}

export function loadedFields(
  fields: readonly AdminScreenField[],
  sections?: readonly AdminScreenSection[],
): AdminScreenViewState {
  return { status: 'loaded', fields, sections };
}

export function loadedMetrics(metrics: readonly AdminScreenMetric[]): AdminScreenViewState {
  return { status: 'loaded', metrics };
}

export function adminDataError(error: unknown): AdminScreenViewState {
  if (error instanceof AdminSessionError && error.code === 'LOGIN_REQUIRED') {
    return {
      status: 'error',
      message: 'Phiên Admin không còn hiệu lực. Hãy đăng nhập lại.',
      retryable: false,
    };
  }
  if (error instanceof HttpErrorResponse) {
    if (error.status === 401) {
      return {
        status: 'error',
        message: 'Phiên Admin đã hết hiệu lực. Hãy đăng nhập lại.',
        httpStatus: error.status,
        retryable: false,
      };
    }
    if (error.status === 403) {
      return {
        status: 'error',
        message: 'Tài khoản không được phép xem dữ liệu này.',
        httpStatus: error.status,
        retryable: false,
      };
    }
    if (error.status === 404) {
      return {
        status: 'error',
        message: 'Không tìm thấy dữ liệu được yêu cầu.',
        httpStatus: error.status,
        retryable: false,
      };
    }
    if (error.status === 422) {
      return {
        status: 'error',
        message: 'Study Server từ chối một hoặc nhiều bộ lọc.',
        httpStatus: error.status,
        retryable: false,
      };
    }
    if (error.status === 0) {
      return {
        status: 'error',
        message: 'Không thể kết nối tới Study Server.',
        httpStatus: error.status,
        retryable: true,
      };
    }
    return {
      status: 'error',
      message: 'Study Server không thể tải dữ liệu lúc này.',
      httpStatus: error.status,
      retryable: true,
    };
  }
  return {
    status: 'error',
    message: 'Study Server không thể tải dữ liệu lúc này.',
    retryable: true,
  };
}

export function formatDate(value: string | null): string {
  if (!value) {
    return '—';
  }
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat('vi-VN').format(date);
}

export function displayValue(value: string | number | null | undefined): string {
  return value === null || value === undefined || value === '' ? '—' : String(value);
}
