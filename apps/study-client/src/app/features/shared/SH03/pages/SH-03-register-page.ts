import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DestroyRef } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, inject, signal, viewChild } from '@angular/core';
import { Router } from '@angular/router';

import { VerificationHandoffStore } from '../../verification-handoff';
import { RegisterApi } from '../data-access/SH-03-register.service';
import { validateRegistration } from '../models/validate-registration';
import type {
  RegistrationAlert,
  RegistrationField,
  RegistrationFieldErrors,
  RegistrationInput,
} from '../models/SH-03-register.models';
import { RegisterView } from '../ui/SH-03-register-view';

@Component({
  selector: 'study-register-page',
  imports: [RegisterView],
  templateUrl: './SH-03-register-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RegisterPage {
  private readonly destroyRef = inject(DestroyRef);
  private readonly api = inject(RegisterApi);
  private readonly router = inject(Router);
  private readonly handoff = inject(VerificationHandoffStore);
  private readonly view = viewChild(RegisterView);

  readonly submitting = signal(false);
  readonly created = signal(false);
  readonly alert = signal<RegistrationAlert | null>(null);
  readonly fieldErrors = signal<RegistrationFieldErrors>({});

  clearField(field: RegistrationField): void {
    this.fieldErrors.update((errors) => ({ ...errors, [field]: undefined }));
    this.alert.set(null);
  }

  submit(input: RegistrationInput): void {
    if (this.submitting() || this.created()) return;

    this.alert.set(null);
    const { request, errors } = validateRegistration(input);
    this.fieldErrors.set(errors);
    const firstError = this.firstError(errors);
    if (firstError) {
      queueMicrotask(() => this.view()?.focusField(firstError));
      return;
    }

    this.submitting.set(true);
    this.api
      .register(request)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          this.submitting.set(false);
          const result = response.body;
          const user = result?.data;
          if (
            response.status !== 201 ||
            result?.success !== true ||
            result.businessCode !== 'DESIGN_RESOURCE_CREATED' ||
            !user ||
            !Number.isSafeInteger(user.id) ||
            user.id <= 0 ||
            typeof user.email !== 'string' ||
            !user.email
          ) {
            this.alert.set({
              title: 'Chưa thể hoàn tất đăng ký',
              description:
                'Phản hồi tạo tài khoản chưa đủ thông tin. Vui lòng kiểm tra trước khi gửi lại.',
              kind: 'warning',
            });
            return;
          }

          this.created.set(true);
          this.handoff.set({ userId: user.id, email: user.email });
          void this.router
            .navigateByUrl('/register/verification')
            .then((navigated) => {
              if (!navigated) this.showNavigationFailure();
            })
            .catch(() => this.showNavigationFailure());
        },
        error: (error: unknown) => {
          this.submitting.set(false);
          this.handleError(error);
        },
      });
  }

  private showNavigationFailure(): void {
    this.handoff.clear();
    this.alert.set({
      title: 'Tài khoản đã được tạo',
      description: 'Chưa mở được bước tiếp theo. Bạn có thể chuyển tới trang đăng nhập.',
      kind: 'success',
    });
  }
  private handleError(error: unknown): void {
    if (!(error instanceof HttpErrorResponse)) {
      this.alert.set({
        title: 'Chưa rõ kết quả đăng ký',
        description: 'Không nhận được phản hồi. Vui lòng kiểm tra trước khi gửi lại.',
        kind: 'warning',
      });
      return;
    }

    const envelope = error.error;
    if (error.status === 409 && envelope?.businessCode === 'DESIGN_STATE_CONFLICT') {
      this.fieldErrors.set({ email: 'Email đã tồn tại.' });
      queueMicrotask(() => this.view()?.focusField('email'));
      return;
    }

    if (error.status === 422 && envelope?.businessCode === 'DESIGN_VALIDATION_ERROR') {
      const errors: RegistrationFieldErrors = {};
      if (Array.isArray(envelope?.meta?.fieldErrors)) {
        for (const detail of envelope.meta.fieldErrors) {
          if (detail?.field === 'full_name') errors.fullName = 'Họ và tên không hợp lệ.';
          if (detail?.field === 'email') errors.email = 'Địa chỉ email không hợp lệ.';
          if (detail?.field === 'password') errors.password = 'Mật khẩu không hợp lệ.';
        }
      }
      this.fieldErrors.set(errors);
      const firstError = this.firstError(errors);
      if (firstError) {
        queueMicrotask(() => this.view()?.focusField(firstError));
        return;
      }
      this.alert.set({
        title: 'Thông tin chưa hợp lệ',
        description: 'Vui lòng kiểm tra lại thông tin đã nhập.',
        kind: 'error',
      });
      return;
    }

    this.alert.set(
      error.status === 0
        ? {
            title: 'Chưa rõ kết quả đăng ký',
            description: 'Không nhận được phản hồi. Vui lòng kiểm tra trước khi gửi lại.',
            kind: 'warning',
          }
        : {
            title: 'Không thể tạo tài khoản',
            description: 'Hệ thống chưa xử lý được yêu cầu. Vui lòng thử lại sau.',
            kind: 'error',
          },
    );
  }

  private firstError(errors: RegistrationFieldErrors): RegistrationField | null {
    if (errors.fullName) return 'fullName';
    if (errors.email) return 'email';
    if (errors.password) return 'password';
    return null;
  }
}
