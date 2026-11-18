import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DestroyRef } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, inject, signal, viewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthSessionService } from '../../../../core/auth/auth-session.service';

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
  private readonly session = inject(AuthSessionService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);
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

          if (!this.session.setSession(response.data)) {
            this.submitting.set(false);
            this.setGeneralError('Phản hồi đăng nhập thiếu thông tin phiên hợp lệ.');
            return;
          }

          const role = this.session.role();
          if (role === 'STUDENT') {
            this.api.currentStudent().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
              next: (profile) => {
                this.submitting.set(false);
                if (!profile.success || !profile.data) {
                  this.session.clear();
                  this.setGeneralError('Không thể xác nhận hồ sơ học viên. Vui lòng đăng nhập lại.');
                  return;
                }
                this.navigateAfterLogin('/student');
              },
              error: (error: unknown) => {
                this.submitting.set(false);
                if (error instanceof HttpErrorResponse && error.status === 403) return;
                this.session.clear();
                this.setGeneralError('Không thể xác nhận hồ sơ học viên. Vui lòng thử lại sau.');
              },
            });
            return;
          }
          this.submitting.set(false);
          this.navigateAfterLogin(role === 'ADMIN' ? '/admin' : '/forbidden');
        },
        error: (error: unknown) => {
          this.submitting.set(false);
          this.handleError(error);
        },
      });
  }

  private navigateAfterLogin(destination: string): void {
    const requested = this.route.snapshot.queryParamMap.get('returnUrl');
    const safeReturn = requested && requested.startsWith(destination) &&
      (requested.length === destination.length || requested[destination.length] === '/' || requested[destination.length] === '?');
    void this.router.navigateByUrl(safeReturn ? requested : destination);
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
