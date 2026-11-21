import { HttpErrorResponse } from '@angular/common/http';
import { Component, DestroyRef, Injector, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Router } from '@angular/router';
import { finalize } from 'rxjs';

import { SH02LoginError, SH02LoginService } from '../data-access/sh02-login.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';

interface LoginFeedback {
  readonly title: string;
  readonly message: string;
}

@Component({
  imports: [StudyIcon],
  selector: 'study-sh02-page',
  templateUrl: './sh02-page.html',
  styleUrl: './sh02-page.css',
})
export class SH02Page {
  private readonly injector = inject(Injector);
  private readonly destroyRef = inject(DestroyRef);

  readonly passwordVisible = signal(false);
  readonly isSubmitting = signal(false);
  readonly loginError = signal<LoginFeedback | null>(null);
  readonly emailError = signal<string | null>(null);
  readonly passwordError = signal<string | null>(null);

  togglePasswordVisibility(): void {
    this.passwordVisible.update((visible) => !visible);
  }

  submitCredentials(
    event: SubmitEvent,
    form: HTMLFormElement,
    emailInput: HTMLInputElement,
    passwordInput: HTMLInputElement,
  ): void {
    event.preventDefault();
    if (this.isSubmitting()) return;

    emailInput.value = emailInput.value.trim();
    passwordInput.setCustomValidity(
      passwordInput.value.trim() ? '' : 'Mật khẩu không được để trống.',
    );
    const isFormValid = form.reportValidity();
    passwordInput.setCustomValidity('');
    if (!isFormValid) return;

    this.loginError.set(null);
    this.emailError.set(null);
    this.passwordError.set(null);
    this.isSubmitting.set(true);

    this.injector
      .get(SH02LoginService)
      .login(emailInput.value, passwordInput.value)
      .pipe(takeUntilDestroyed(this.destroyRef), finalize(() => this.isSubmitting.set(false)))
      .subscribe({
        next: (destination) => {
          passwordInput.value = '';
          void this.injector.get(Router).navigateByUrl(destination);
        },
        error: (error: unknown) => {
          const feedback = presentLoginError(error);
          this.loginError.set(feedback);
          this.emailError.set(feedback.fieldErrors.email);
          this.passwordError.set(feedback.fieldErrors.password);
        },
      });
  }

  clearFieldError(field: 'email' | 'password'): void {
    if (field === 'email') this.emailError.set(null);
    else this.passwordError.set(null);
  }
}

function presentLoginError(error: unknown): {
  readonly title: string;
  readonly message: string;
  readonly fieldErrors: { email: string | null; password: string | null };
} {
  const fieldErrors = readFieldErrors(error);

  if (error instanceof SH02LoginError) {
    if (error.code === 'UNSUPPORTED_ROLE') {
      return {
        title: 'Không thể mở khu vực tài khoản',
        message: 'Vai trò tài khoản này chưa có khu vực phù hợp trong Study LMS.',
        fieldErrors,
      };
    }
    if (error.code === 'STUDENT_PROFILE_MISMATCH') {
      return {
        title: 'Không thể xác minh hồ sơ học viên',
        message: 'Hãy thử đăng nhập lại sau ít phút.',
        fieldErrors,
      };
    }
  }

  if (error instanceof HttpErrorResponse) {
    const envelope = asRecord(error.error);
    const businessCode = envelope?.['businessCode'];
    const serverMessage =
      typeof envelope?.['message'] === 'string' ? envelope['message'].trim() : '';

    if (error.status === 401 && businessCode === 'DESIGN_AUTHENTICATION_REQUIRED') {
      return {
        title: 'Thông tin đăng nhập chưa chính xác',
        message: serverMessage || 'Kiểm tra email và mật khẩu rồi thử lại.',
        fieldErrors,
      };
    }
    if (error.status === 403 && businessCode === 'DESIGN_ACCESS_DENIED') {
      return {
        title: 'Tài khoản chưa thể đăng nhập',
        message: serverMessage || 'Tài khoản hiện không được phép đăng nhập.',
        fieldErrors,
      };
    }
    if (error.status === 422 && businessCode === 'DESIGN_VALIDATION_ERROR') {
      return {
        title: 'Kiểm tra lại thông tin',
        message: serverMessage || 'Một số thông tin chưa hợp lệ.',
        fieldErrors,
      };
    }
    if (error.status === 0) {
      return {
        title: 'Không thể kết nối',
        message: 'Không thể kết nối tới Study Server. Hãy thử lại.',
        fieldErrors,
      };
    }
  }

  return {
    title: 'Không thể đăng nhập',
    message: 'Đã xảy ra lỗi. Hãy thử lại sau ít phút.',
    fieldErrors,
  };
}

function readFieldErrors(error: unknown): { email: string | null; password: string | null } {
  if (!(error instanceof HttpErrorResponse)) return { email: null, password: null };
  const envelope = asRecord(error.error);
  const meta = asRecord(envelope?.['meta']);
  const rawErrors = meta?.['fieldErrors'];
  const result: { email: string | null; password: string | null } = {
    email: null,
    password: null,
  };
  if (!Array.isArray(rawErrors)) return result;

  for (const value of rawErrors) {
    const fieldError = asRecord(value);
    const field = fieldError?.['field'];
    const message = fieldError?.['message'];
    if (typeof message !== 'string' || !message.trim()) continue;
    if (field === 'email' && result.email === null) result.email = message;
    if (field === 'password' && result.password === null) result.password = message;
  }
  return result;
}

function asRecord(value: unknown): Record<string, unknown> | null {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : null;
}
