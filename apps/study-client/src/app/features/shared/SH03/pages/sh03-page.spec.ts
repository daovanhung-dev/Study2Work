import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import type { ComponentFixture } from '@angular/core/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { SH03Page } from './sh03-page';

describe('SH03Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SH03Page],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('renders the required registration fields with submit enabled', () => {
    const fixture = TestBed.createComponent(SH03Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const fullName = root.querySelector<HTMLInputElement>('#register-fullname');
    const email = root.querySelector<HTMLInputElement>('#register-email');
    const password = root.querySelector<HTMLInputElement>('#register-password');
    const submit = root.querySelector<HTMLButtonElement>('.submit-button');

    expect(root.querySelector('h1')?.textContent?.trim()).toBe('Đăng ký tài khoản học viên');
    expect(fullName?.name).toBe('fullname');
    expect(email?.name).toBe('email');
    expect(email?.type).toBe('email');
    expect(password?.name).toBe('password');
    expect(password?.type).toBe('password');
    expect(password?.minLength).toBe(-1);
    expect(submit?.disabled).toBe(false);
    expect(root.querySelector('#register-unavailable')).toBeNull();
    expect(root.querySelector('a[href="/login"]')?.textContent).toContain('Đăng nhập');
  });

  it('rejects blank or whitespace-only values locally without making a request', () => {
    const fixture = TestBed.createComponent(SH03Page);
    fixture.detectChanges();
    submit(fixture);

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('#register-fullname-error')?.textContent).toContain('không được để trống');
    expect(root.querySelector('#register-email-error')?.textContent).toContain('không được để trống');
    expect(root.querySelector('#register-password-error')?.textContent).toContain('không được để trống');
    http.expectNone('/api/v1/auth/register');
  });

  it('rejects an invalid email locally without making a request', () => {
    const fixture = TestBed.createComponent(SH03Page);
    fixture.detectChanges();
    setInput(fixture, '#register-fullname', 'Nguyen Van A');
    setInput(fixture, '#register-email', 'not-an-email');
    setInput(fixture, '#register-password', 'password');
    submit(fixture);

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('#register-email-error')?.textContent).toContain(
      'không đúng định dạng',
    );
    http.expectNone('/api/v1/auth/register');
  });

  it('trims name/email, preserves password, prevents duplicate submit and handles a 201 response', () => {
    const fixture = TestBed.createComponent(SH03Page);
    fixture.detectChanges();
    setInput(fixture, '#register-fullname', '  Nguyen Van A  ');
    setInput(fixture, '#register-email', ' student@example.com ');
    setInput(fixture, '#register-password', '  keep this password  ');

    submit(fixture);
    submit(fixture);

    const requests = http.match('/api/v1/auth/register');
    expect(requests).toHaveLength(1);
    const request = requests[0];
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual({
      email: 'student@example.com',
      password: '  keep this password  ',
      full_name: 'Nguyen Van A',
    });
    expect(request.request.headers.has('Authorization')).toBe(false);
    expect((fixture.nativeElement as HTMLElement).querySelector('.submit-button')?.hasAttribute('disabled'))
      .toBe(true);
    http.expectNone('/api/v1/auth/register');

    request.flush(successEnvelope({ id: 1001, email: 'student@example.com' }), {
      status: 201,
      statusText: 'Created',
    });
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Tài khoản đã được tạo.');
    expect(root.textContent).toContain('chưa xác nhận email đã được gửi');
    expect(root.querySelector('a[href="/register/verification"]')?.textContent).toContain(
      'Xem thông tin về xác minh email',
    );
    expect(root.querySelector('#register-password')).toBeNull();
    http.expectNone('/api/v1/auth/verify-email/send');
  });

  it.each([
    { caseName: 'missing id', status: 201, data: { email: 'student@example.com' } },
    { caseName: 'missing email', status: 201, data: { id: 1001 } },
    {
      caseName: 'unexpected HTTP 200 status',
      status: 200,
      data: { id: 1001, email: 'student@example.com' },
    },
  ])('does not claim success for $caseName', ({ status, data }) => {
    const fixture = TestBed.createComponent(SH03Page);
    fixture.detectChanges();
    setInput(fixture, '#register-fullname', 'Nguyen Van A');
    setInput(fixture, '#register-email', 'student@example.com');
    setInput(fixture, '#register-password', 'password');
    submit(fixture);

    http.expectOne('/api/v1/auth/register').flush(successEnvelope(data), {
      status,
      statusText: status === 201 ? 'Created' : 'OK',
    });
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('.registration-result')).toBeNull();
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Chưa thể xác nhận kết quả đăng ký',
    );
    expect(root.querySelector<HTMLInputElement>('#register-password')?.value).toBe('password');
    http.expectNone('/api/v1/auth/verify-email/send');
  });

  it('maps duplicate email to the email field and keeps entered values', () => {
    const fixture = TestBed.createComponent(SH03Page);
    fixture.detectChanges();
    setInput(fixture, '#register-fullname', 'Nguyen Van A');
    setInput(fixture, '#register-email', 'student@example.com');
    setInput(fixture, '#register-password', 'password');
    submit(fixture);

    http.expectOne('/api/v1/auth/register').flush(
      errorEnvelope('DESIGN_STATE_CONFLICT', 'Email đã tồn tại.'),
      { status: 409, statusText: 'Conflict' },
    );
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('#register-email-error')?.textContent).toContain('Email đã tồn tại.');
    expect(root.querySelector<HTMLInputElement>('#register-email')?.value).toBe('student@example.com');
    expect(root.textContent).not.toContain('database unavailable');
  });

  it('maps validation field errors and does not render raw server messages', () => {
    const fixture = TestBed.createComponent(SH03Page);
    fixture.detectChanges();
    setInput(fixture, '#register-fullname', 'Nguyen Van A');
    setInput(fixture, '#register-email', 'student@example.com');
    setInput(fixture, '#register-password', 'password');
    submit(fixture);

    http.expectOne('/api/v1/auth/register').flush(
      {
        ...errorEnvelope('DESIGN_VALIDATION_ERROR', 'Raw internal detail'),
        meta: {
          fieldErrors: [
            { field: 'full_name', code: 'STRING_TOO_LONG', message: 'Raw validation detail' },
            { field: 'password', code: 'VALUE_ERROR', message: 'Raw password detail' },
          ],
        },
      },
      { status: 422, statusText: 'Unprocessable Content' },
    );
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('#register-fullname-error')?.textContent).toContain('không hợp lệ');
    expect(root.querySelector('#register-password-error')?.textContent).toContain('không hợp lệ');
    expect(root.textContent).not.toContain('Raw internal detail');
    expect(root.textContent).not.toContain('Raw validation detail');
  });

  it('shows a safe server error and never exposes the response detail', () => {
    const fixture = TestBed.createComponent(SH03Page);
    fixture.detectChanges();
    setInput(fixture, '#register-fullname', 'Nguyen Van A');
    setInput(fixture, '#register-email', 'student@example.com');
    setInput(fixture, '#register-password', 'password');
    submit(fixture);

    http.expectOne('/api/v1/auth/register').flush(
      errorEnvelope('DESIGN_INTERNAL_ERROR', 'database unavailable'),
      { status: 500, statusText: 'Internal Server Error' },
    );
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent).toContain('Không thể tạo tài khoản');
    expect(root.textContent).not.toContain('database unavailable');
  });

  it('reports an unknown network outcome without automatically retrying', () => {
    const fixture = TestBed.createComponent(SH03Page);
    fixture.detectChanges();
    setInput(fixture, '#register-fullname', 'Nguyen Van A');
    setInput(fixture, '#register-email', 'student@example.com');
    setInput(fixture, '#register-password', 'password');
    submit(fixture);

    http.expectOne('/api/v1/auth/register').error(new ProgressEvent('error'));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent).toContain('Kết quả đăng ký chưa xác định');
    http.expectNone('/api/v1/auth/register');
  });
});

function setInput(fixture: ComponentFixture<SH03Page>, selector: string, value: string): void {
  const root = fixture.nativeElement as HTMLElement;
  const input = root.querySelector<HTMLInputElement>(selector);
  if (!input) throw new Error(`Missing input ${selector}`);
  input.value = value;
  input.dispatchEvent(new Event('input', { bubbles: true }));
  fixture.detectChanges();
}

function submit(fixture: ComponentFixture<SH03Page>): void {
  const form = fixture.nativeElement.querySelector('form') as HTMLFormElement | null;
  if (!form) throw new Error('Missing registration form');
  form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
  fixture.detectChanges();
}

function successEnvelope(data: unknown): ApiEnvelope<unknown> {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_CREATED',
    message: 'Tạo tài khoản thành công.',
    data,
    meta: {},
    traceId: 'trace-id',
  };
}

function errorEnvelope(
  businessCode: string,
  message: string,
): ApiEnvelope<unknown> {
  return {
    success: false,
    businessCode,
    message,
    data: null,
    meta: {},
    traceId: 'trace-id',
  };
}
