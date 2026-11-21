import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DestroyRef } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, inject, signal, viewChild } from '@angular/core';
import { Router } from '@angular/router';
import { take } from 'rxjs';

import { StudyAuthSessionService } from '../../../../core/auth/study-auth-session.service';
import { StudentAccountProfileService } from '../../../student/data-access/student-profile.service';
import { LoginApi } from '../data-access/SH-02-login.service';
import type { LoginAlert, LoginCredentials, LoginFieldErrors } from '../models/SH-02-login.models';
import { LoginView } from '../ui/SH-02-login-view';

@Component({
  selector: 'study-login-page',
  imports: [LoginView],
  templateUrl: './SH-02-login-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LoginPage {
  private readonly destroyRef = inject(DestroyRef);
  private readonly api = inject(LoginApi);
  private readonly session = inject(StudyAuthSessionService);
  private readonly profileApi = inject(StudentAccountProfileService);
  private readonly router = inject(Router);
  private readonly view = viewChild(LoginView);

  readonly submitting = signal(false);
  readonly alert = signal<LoginAlert | null>(null);
  readonly fieldErrors = signal<LoginFieldErrors>({});

  clearErrors(): void {
    this.alert.set(null);
    this.fieldErrors.set({});
  }

  submit(credentials: LoginCredentials): void {
    if (this.submitting()) return;

    this.clearErrors();

    const fieldErrors: LoginFieldErrors = {};
    if (!credentials.email.trim()) {
      fieldErrors.email = 'Vui lòng nhập địa chỉ email.';
    }
    if (!credentials.password.trim()) {
      fieldErrors.password = 'Vui lòng nhập mật khẩu.';
    }
    if (fieldErrors.email || fieldErrors.password) {
      this.fieldErrors.set(fieldErrors);
      queueMicrotask(() => this.view()?.focusField(fieldErrors.email ? 'email' : 'password'));
      return;
    }

    this.submitting.set(true);
    this.api
      .login({ email: credentials.email.trim(), password: credentials.password })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          if (!response || response.success !== true || !response.data) {
            this.submitting.set(false);
            this.alert.set({
              title: 'Không thể hoàn tất đăng nhập',
              description: 'Phản hồi từ hệ thống chưa đúng định dạng. Vui lòng thử lại sau.',
              kind: 'error',
            });
            return;
          }

          const auth = response.data;
          if (
            typeof auth.access_token !== 'string' ||
            !auth.access_token ||
            typeof auth.role !== 'string' ||
            auth.role.toUpperCase() !== 'STUDENT'
          ) {
            this.finishRejectedLogin();
            return;
          }

          this.session.setAccessToken(auth.access_token);
          this.profileApi
            .getProfile()
            .pipe(take(1), takeUntilDestroyed(this.destroyRef))
            .subscribe({
              next: (profile) => {
                if (profile.role.toUpperCase() !== 'STUDENT') {
                  this.finishRejectedLogin();
                  return;
                }
                this.session.markStudentProfileVerified();
                this.submitting.set(false);
                this.session.broadcastSessionChange();
                void this.router.navigateByUrl('/student');
              },
              error: () => this.finishFailedHandoff(),
            });
        },
        error: (error: unknown) => {
          this.submitting.set(false);
          this.handleError(error);
        },
      });
  }

  private finishRejectedLogin(): void {
    this.session.clearAccessToken();
    this.session
      .logout()
      .pipe(take(1), takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.submitting.set(false);
          void this.router.navigateByUrl('/forbidden');
        },
        error: () => {
          this.submitting.set(false);
          void this.router.navigateByUrl('/forbidden');
        },
      });
  }

  private finishFailedHandoff(): void {
    this.session.clearAccessToken();
    this.session
      .logout()
      .pipe(take(1), takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.submitting.set(false);
          this.setGeneralError('Không thể xác minh hồ sơ người học. Vui lòng đăng nhập lại.');
        },
        error: () => {
          this.submitting.set(false);
          this.setGeneralError('Không thể hoàn tất phiên đăng nhập. Vui lòng thử lại.');
        },
      });
  }

  private handleError(error: unknown): void {
    if (!(error instanceof HttpErrorResponse)) {
      this.setGeneralError('Không thể kết nối đến hệ thống. Vui lòng thử lại sau.');
      return;
    }

    if (error.status === 422) {
      const details = error.error?.meta?.fieldErrors;
      const fieldErrors: LoginFieldErrors = {};
      if (Array.isArray(details)) {
        for (const detail of details) {
          if (detail?.field === 'email') fieldErrors.email = 'Địa chỉ email không hợp lệ.';
          if (detail?.field === 'password') fieldErrors.password = 'Mật khẩu không hợp lệ.';
        }
      }
      if (fieldErrors.email || fieldErrors.password) {
        this.fieldErrors.set(fieldErrors);
        queueMicrotask(() => this.view()?.focusField(fieldErrors.email ? 'email' : 'password'));
        return;
      }
      this.setGeneralError('Thông tin nhập chưa hợp lệ. Vui lòng kiểm tra lại.');
      return;
    }

    if (error.status === 401) {
      this.setGeneralError('Email hoặc mật khẩu không đúng.', 'Đăng nhập không thành công');
    } else if (error.status === 403) {
      this.setGeneralError('Tài khoản không được phép đăng nhập.', 'Không thể truy cập');
    } else {
      this.setGeneralError('Không thể xử lý đăng nhập lúc này. Vui lòng thử lại sau.');
    }
  }

  private setGeneralError(description: string, title = 'Không thể đăng nhập'): void {
    this.alert.set({ title, description, kind: 'error' });
  }
}
