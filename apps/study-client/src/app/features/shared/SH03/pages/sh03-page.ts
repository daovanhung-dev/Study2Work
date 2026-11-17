import { HttpErrorResponse } from '@angular/common/http';
import { Component, ElementRef, inject, signal } from '@angular/core';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  type ValidatorFn,
  Validators,
} from '@angular/forms';
import { RouterLink } from '@angular/router';
import { finalize } from 'rxjs';

import { SH03RegistrationService } from '../data-access/sh03-registration.service';
import type {
  SH03RegistrationField,
  SH03RegistrationFieldErrors,
  SH03RegistrationRequest,
  SH03RegistrationResult,
} from '../models/sh03-registration.models';

@Component({
  imports: [ReactiveFormsModule, RouterLink],
  selector: 'study-sh03-page',
  templateUrl: './sh03-page.html',
  styleUrl: './sh03-page.css',
})
export class SH03Page {
  private readonly registrationService = inject(SH03RegistrationService);
  private readonly element = inject(ElementRef<HTMLElement>);

  readonly registrationForm = new FormGroup({
    fullName: new FormControl('', {
      nonNullable: true,
      validators: [requiredAfterTrim(), maxLengthAfterTrim(150)],
    }),
    email: new FormControl('', {
      nonNullable: true,
      validators: [requiredAfterTrim(), emailFormatAfterTrim(), maxLengthAfterTrim(255)],
    }),
    password: new FormControl('', {
      nonNullable: true,
      validators: [requiredAfterTrim()],
    }),
  });

  readonly isSubmitting = signal(false);
  readonly registrationCreated = signal(false);
  readonly attemptedSubmit = signal(false);
  readonly generalError = signal<string | null>(null);
  readonly fieldErrors = signal<SH03RegistrationFieldErrors>({});

  submit(): void {
    if (this.isSubmitting() || this.registrationCreated()) return;

    this.attemptedSubmit.set(true);
    this.generalError.set(null);
    this.fieldErrors.set({});

    if (this.registrationForm.invalid) {
      this.registrationForm.markAllAsTouched();
      this.focusFirstInvalidField();
      return;
    }

    const values = this.registrationForm.getRawValue();
    const request: SH03RegistrationRequest = {
      email: values.email.trim(),
      password: values.password,
      full_name: values.fullName.trim(),
    };

    this.isSubmitting.set(true);
    this.registrationService
      .register(request)
      .pipe(finalize(() => this.isSubmitting.set(false)))
      .subscribe({
        next: (httpResponse) => {
          const response = httpResponse.body;
          if (
            httpResponse.status === 201 &&
            response?.success &&
            response.businessCode === 'DESIGN_RESOURCE_CREATED' &&
            isRegistrationResult(response.data)
          ) {
            this.registrationCreated.set(true);
            this.registrationForm.controls.password.reset('');
            return;
          }

          this.generalError.set(
            'Chưa thể xác nhận kết quả đăng ký. Hãy kiểm tra trạng thái trước khi gửi lại.',
          );
        },
        error: (error: unknown) => this.handleRequestError(error),
      });
  }

  fieldMessage(field: SH03RegistrationField): string | null {
    const serverMessage = this.fieldErrors()[field];
    if (serverMessage) return serverMessage;

    const control = this.registrationForm.controls[field];
    if (!this.attemptedSubmit() && !control.touched) return null;
    if (control.hasError('required')) {
      return field === 'fullName'
        ? 'Họ và tên không được để trống.'
        : field === 'email'
          ? 'Địa chỉ email không được để trống.'
          : 'Mật khẩu không được để trống.';
    }
    if (control.hasError('maxlength')) {
      return field === 'fullName'
        ? 'Họ và tên không được vượt quá 150 ký tự.'
        : 'Địa chỉ email không được vượt quá 255 ký tự.';
    }
    if (control.hasError('email')) {
      return 'Địa chỉ email không đúng định dạng.';
    }
    return null;
  }

  clearFieldError(field: SH03RegistrationField): void {
    this.fieldErrors.update((errors) => {
      const next = { ...errors };
      delete next[field];
      return next;
    });
    this.generalError.set(null);
  }

  private handleRequestError(error: unknown): void {
    if (!(error instanceof HttpErrorResponse)) {
      this.generalError.set('Không thể hoàn tất đăng ký lúc này. Vui lòng thử lại sau.');
      return;
    }

    const body = asRecord(error.error);
    const businessCode = body?.['businessCode'];

    if (error.status === 409 && businessCode === 'DESIGN_STATE_CONFLICT') {
      this.fieldErrors.set({ email: 'Email đã tồn tại.' });
      this.focusField('email');
      return;
    }

    if (error.status === 422 && businessCode === 'DESIGN_VALIDATION_ERROR') {
      const mappedErrors = mapFieldErrors(body?.['meta']);
      this.fieldErrors.set(mappedErrors.errors);
      if (mappedErrors.firstField) this.focusField(mappedErrors.firstField);
      if (Object.keys(mappedErrors.errors).length === 0) {
        this.generalError.set('Thông tin đăng ký chưa hợp lệ. Vui lòng kiểm tra lại.');
      }
      return;
    }

    if (error.status === 0) {
      this.generalError.set(
        'Chưa nhận được phản hồi. Kết quả đăng ký chưa xác định; hãy kiểm tra trạng thái trước khi gửi lại.',
      );
      return;
    }

    this.generalError.set('Không thể tạo tài khoản lúc này. Vui lòng thử lại sau.');
  }

  private focusFirstInvalidField(): void {
    const firstInvalid = (['fullName', 'email', 'password'] as const).find(
      (field) => this.registrationForm.controls[field].invalid,
    );
    if (firstInvalid) this.focusField(firstInvalid);
  }

  private focusField(field: SH03RegistrationField): void {
    const inputId = field === 'fullName' ? 'register-fullname' : `register-${field}`;
    const host = this.element.nativeElement as HTMLElement;
    host.querySelector<HTMLInputElement>(`#${inputId}`)?.focus();
  }
}

function requiredAfterTrim(): ValidatorFn {
  return (control) =>
    typeof control.value === 'string' && control.value.trim().length === 0
      ? { required: true }
      : null;
}

function maxLengthAfterTrim(maxLength: number): ValidatorFn {
  return (control) => {
    if (typeof control.value !== 'string') return null;
    const actualLength = control.value.trim().length;
    return actualLength > maxLength
      ? { maxlength: { requiredLength: maxLength, actualLength } }
      : null;
  };
}

function emailFormatAfterTrim(): ValidatorFn {
  return (control) => {
    if (typeof control.value !== 'string' || control.value.trim().length === 0) return null;

    return Validators.email(
      new FormControl(control.value.trim(), { nonNullable: true }),
    );
  };
}

function asRecord(value: unknown): Record<string, unknown> | null {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : null;
}

function isRegistrationResult(value: unknown): value is SH03RegistrationResult {
  const result = asRecord(value);
  const id = result?.['id'];
  const email = result?.['email'];

  return (
    typeof id === 'number' &&
    Number.isInteger(id) &&
    id > 0 &&
    typeof email === 'string' &&
    email.trim().length > 0
  );
}

function mapFieldErrors(meta: unknown): {
  errors: SH03RegistrationFieldErrors;
  firstField: SH03RegistrationField | null;
} {
  const metadata = asRecord(meta);
  const rawErrors = metadata?.['fieldErrors'];
  if (!Array.isArray(rawErrors)) return { errors: {}, firstField: null };

  const errors: SH03RegistrationFieldErrors = {};
  for (const rawError of rawErrors) {
    const item = asRecord(rawError);
    const field = mapFieldName(item?.['field']);
    if (!field || errors[field]) continue;
    errors[field] = fieldErrorMessage(field);
  }

  const firstField = (Object.keys(errors) as SH03RegistrationField[])[0] ?? null;
  return { errors, firstField };
}

function mapFieldName(field: unknown): SH03RegistrationField | null {
  switch (field) {
    case 'full_name':
    case 'fullname':
      return 'fullName';
    case 'email':
      return 'email';
    case 'password':
      return 'password';
    default:
      return null;
  }
}

function fieldErrorMessage(field: SH03RegistrationField): string {
  switch (field) {
    case 'fullName':
      return 'Họ và tên không hợp lệ.';
    case 'email':
      return 'Địa chỉ email không hợp lệ.';
    case 'password':
      return 'Mật khẩu không hợp lệ.';
  }
}
