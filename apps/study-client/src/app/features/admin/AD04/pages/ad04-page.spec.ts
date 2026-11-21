import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, type ParamMap } from '@angular/router';
import { BehaviorSubject, firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminUserProfile } from '../../admin-api.models';
import { AD04Page } from './ad04-page';

describe('AD04Page', () => {
  let http: HttpTestingController;
  let routeParams: BehaviorSubject<ParamMap>;

  beforeEach(async () => {
    routeParams = new BehaviorSubject(convertToParamMap({ userId: '9007199254740993' }));
    await TestBed.configureTestingModule({
      imports: [AD04Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([]),
        { provide: ActivatedRoute, useValue: { paramMap: routeParams.asObservable() } },
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('loads only #69 using the exact route ID and displays its profile projection', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD04Page);
    fixture.detectChanges();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Đang tải hồ sơ');
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/users/9007199254740993');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope(profile()));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('User Name');
    expect(root.textContent).toContain('user@example.test');
    expect(root.textContent).toContain('MENTOR');
    expect(root.textContent).toContain('ACTIVE');
    expect(root.querySelector<HTMLInputElement>('#user-phone')?.value).toBe('0900000000');
    expect(root.querySelector<HTMLInputElement>('#user-avatar-url')?.value).toBe('https://media.example.test/avatar.png');
    expect(root.textContent).toContain('User ID từ đường dẫn: 9007199254740993');
    expect(root.querySelectorAll('a[href="/admin/users/9007199254740993"]')).toHaveLength(2);
    expect(root.querySelector('img, picture, video, iframe')).toBeNull();
    http.expectNone((candidate) => candidate.method !== 'GET');
  });

  it('keeps all profile controls and Save disabled and never calls #70', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD04Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/users/9007199254740993').flush(successEnvelope(profile()));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const inputs = [...root.querySelectorAll<HTMLInputElement>('input')];
    expect(inputs).toHaveLength(7);
    expect(inputs.every((input) => input.disabled)).toBe(true);
    expect(root.querySelector<HTMLButtonElement>('button')?.disabled).toBe(true);
    expect(root.querySelector('textarea')).toBeNull();
    expect(root.textContent).toContain('adminNotes');
    expect(root.textContent).toContain('PUT chưa được client gọi');
    http.expectNone((candidate) => candidate.method === 'PUT');
    http.expectNone((candidate) => candidate.method === 'PATCH');
  });

  it('shows an error state for an unavailable user and keeps the AD-03 route', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD04Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/users/9007199254740993').flush({
      success: false,
      businessCode: 'DESIGN_RESOURCE_NOT_FOUND',
      message: 'User not found.',
      data: null,
      meta: {},
      traceId: 'test-trace',
    }, { status: 404, statusText: 'Not Found' });
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Không thể tải hồ sơ người dùng');
    expect(root.querySelector('a[href="/admin/users/9007199254740993"]')).not.toBeNull();
    expect(root.querySelector('button')).toBeNull();
  });

  it('does not request a profile when the route has no user ID', async () => {
    routeParams.next(convertToParamMap({}));
    const fixture = TestBed.createComponent(AD04Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Thiếu mã người dùng trên đường dẫn.');
    http.expectNone('/api/v1/admin/users/9007199254740993');
    http.expectNone((candidate) => candidate.url === '/api/v1/admin/users');
  });

  async function signIn(): Promise<void> {
    const login = firstValueFrom(
      TestBed.inject(AdminSessionService).login('admin@example.test', 'password'),
    );
    http.expectOne('/api/v1/auth/login').flush(successEnvelope({
      full_name: 'Admin User',
      email: 'admin@example.test',
      role: 'ADMIN',
      access_token: 'access-token-1',
      refresh_token: 'refresh-token-1',
      token_type: 'bearer',
      expires_in: 60,
      refresh_expires_in: 3600,
    }));
    await login;
  }
});

function profile(overrides: Partial<AdminUserProfile> = {}): AdminUserProfile {
  return {
    id: 77,
    full_name: 'User Name',
    email: 'user@example.test',
    role: 'MENTOR',
    avatar_url: 'https://media.example.test/avatar.png',
    phone: '0900000000',
    status: 'ACTIVE',
    created_at: '2026-01-01T00:00:00Z',
    updated_at: '2026-11-01T00:00:00Z',
    ...overrides,
  };
}

function successEnvelope<T>(data: T): ApiEnvelope<T> {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'ok',
    data,
    meta: {},
    traceId: 'test-trace',
  };
}
