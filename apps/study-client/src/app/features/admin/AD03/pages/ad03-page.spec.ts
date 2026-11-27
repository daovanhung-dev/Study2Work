import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminUserProfile } from '../../admin-api.models';
import { AD03Page } from './ad03-page';

describe('AD03Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AD03Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([{ path: 'admin/users/:userId', component: AD03Page }]),
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('calls API #69 with the route ID and renders the source-backed profile while keeping actions gated', async () => {
    await signIn();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/admin/users/17', AD03Page);
    await harness.fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/users/17');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope(userProfile(17)));
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement!;
    expect(page.viewState().status).toBe('loaded');
    expect(root.querySelector('h1')?.textContent).toContain('Hồ sơ chi tiết tài khoản');
    expect(root.querySelector('.api-state')?.textContent).toContain('API #69 · Đã tải');
    expect(root.querySelector('.identity-list')?.textContent).toContain('Nguyen Thi Mai');
    expect(root.querySelector('.identity-list')?.textContent).toContain('mai@example.test');
    expect(root.querySelector('.identity-list')?.textContent).toContain('+84 900 000 017');
    expect(root.querySelector('.identity-list')?.textContent).toContain('Mã định danh người dùng17');
    expect(root.querySelector('a[href="/admin/users"]')).not.toBeNull();
    expect(root.querySelectorAll('button.action-link')).toHaveLength(2);
    expect(
      Array.from(root.querySelectorAll<HTMLButtonElement>('button.action-link')).every(
        (button) => button.disabled,
      ),
    ).toBe(true);
    expect(root.querySelector('a[href="/admin/users/17/edit"]')).toBeNull();
    expect(root.querySelector('a[href="/admin/users/17/actions"]')).toBeNull();
  });

  it('rejects a malformed route ID without requesting protected user data', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/admin/users/not-an-id', AD03Page);
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement!;
    expect(page.viewState().status).toBe('error');
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Mã người dùng phải là số nguyên signed 64-bit.',
    );
    expect(root.querySelector('.api-state')?.textContent).toContain('Lỗi tải');
    http.expectNone('/api/v1/admin/users/not-an-id');
    http.expectNone('/api/v1/admin/users');
  });

  it('keeps a server failure separate from a loaded profile', async () => {
    await signIn();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/admin/users/17', AD03Page);
    await harness.fixture.whenStable();

    http.expectOne('/api/v1/admin/users/17').flush(
      {
        success: false,
        businessCode: 'DESIGN_INTERNAL_ERROR',
        message: 'failed',
        data: null,
        meta: {},
        traceId: 'test-trace',
      },
      { status: 500, statusText: 'Server Error' },
    );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement!;
    expect(page.viewState().status).toBe('error');
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Study Server không thể tải dữ liệu lúc này.',
    );
    expect(root.querySelector('.api-state')?.textContent).toContain('Lỗi tải');
    expect(root.querySelector('.identity-list')?.textContent).toContain('—');
    expect(root.querySelector('.identity-list')?.textContent).not.toContain('mai@example.test');
    expect(root.querySelectorAll('button.action-link').length).toBe(2);
  });

  it('does not treat a success envelope with a non-#69 business code as loaded data', async () => {
    await signIn();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/admin/users/17', AD03Page);
    await harness.fixture.whenStable();

    http.expectOne('/api/v1/admin/users/17').flush(
      successEnvelope(userProfile(17), 'DESIGN_RESOURCE_NOT_FOUND'),
    );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement!;
    expect(page.viewState().status).toBe('error');
    expect(root.querySelector('[role="alert"]')).not.toBeNull();
    expect(root.querySelector('.identity-list')?.textContent).not.toContain('mai@example.test');
  });

  async function signIn(): Promise<void> {
    const login = firstValueFrom(
      TestBed.inject(AdminSessionService).login('admin@example.test', 'password'),
    );
    http.expectOne('/api/v1/auth/login').flush(
      successEnvelope({
        full_name: 'Admin User',
        email: 'admin@example.test',
        role: 'ADMIN',
        access_token: 'access-token-1',
        refresh_token: 'refresh-token-1',
        token_type: 'bearer',
        expires_in: 60,
        refresh_expires_in: 3600,
      }),
    );
    await login;
  }
});

function successEnvelope<T>(
  data: T,
  businessCode = 'DESIGN_RESOURCE_RETRIEVED',
): ApiEnvelope<T> {
  return {
    success: true,
    businessCode,
    message: 'ok',
    data,
    meta: {},
    traceId: 'test-trace',
  };
}

function userProfile(id: number): AdminUserProfile {
  return {
    id,
    full_name: 'Nguyen Thi Mai',
    email: 'mai@example.test',
    role: 'MENTOR',
    avatar_url: null,
    phone: '+84 900 000 017',
    status: 'ACTIVE',
    created_at: '2026-01-01T00:00:00Z',
    updated_at: '2026-01-02T00:00:00Z',
  };
}
