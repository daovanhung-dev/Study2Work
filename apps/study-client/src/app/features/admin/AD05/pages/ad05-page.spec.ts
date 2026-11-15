import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, type ParamMap } from '@angular/router';
import { BehaviorSubject, firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminUserProfile } from '../../admin-api.models';
import { AD05Page } from './ad05-page';

describe('AD05Page', () => {
  let http: HttpTestingController;
  let routeParams: BehaviorSubject<ParamMap>;

  beforeEach(async () => {
    routeParams = new BehaviorSubject(convertToParamMap({ userId: '9007199254740993' }));
    await TestBed.configureTestingModule({
      imports: [AD05Page],
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

  it('loads #69 with the exact route ID and shows the source status literally', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD05Page);
    fixture.detectChanges();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Đang tải tài khoản');
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/users/9007199254740993');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope(profile()));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('User Name');
    expect(root.textContent).toContain('user@example.test');
    expect(root.textContent).toContain('ACTIVE');
    expect(root.textContent).toContain('MENTOR');
    expect(root.textContent).toContain('User ID từ đường dẫn: 9007199254740993');
    expect(root.querySelectorAll('a[href="/admin/users/9007199254740993"]')).toHaveLength(1);
    http.expectNone((candidate) => candidate.method !== 'GET');
  });

  it('keeps status, delete and reason controls disabled without #71/#72 requests', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD05Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/users/9007199254740993').flush(successEnvelope(profile()));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const buttons = [...root.querySelectorAll<HTMLButtonElement>('button')];
    expect(buttons.map((button) => button.textContent?.trim())).toEqual([
      'Khóa tài khoản',
      'Mở khóa tài khoản',
      'Đánh dấu xóa',
    ]);
    expect(buttons.every((button) => button.disabled)).toBe(true);
    expect(root.querySelector<HTMLTextAreaElement>('textarea')?.disabled).toBe(true);
    expect(root.textContent).toContain('Local suspend thu hồi refresh token');
    expect(root.textContent).toContain('Local #72 không anonymize dữ liệu');
    http.expectNone((candidate) => candidate.method === 'PATCH');
    http.expectNone((candidate) => candidate.method === 'DELETE');
  });

  it('shows a safe not-found state and preserves the AD-03 user ID link', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD05Page);
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
    expect(root.textContent).toContain('Không thể tải tài khoản');
    expect(root.querySelector('a[href="/admin/users/9007199254740993"]')).not.toBeNull();
    expect(root.querySelector('button')).toBeNull();
  });

  it('does not request a profile when the route has no user ID', async () => {
    routeParams.next(convertToParamMap({}));
    const fixture = TestBed.createComponent(AD05Page);
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
    avatar_url: null,
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
