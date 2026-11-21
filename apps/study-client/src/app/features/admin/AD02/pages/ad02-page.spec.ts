import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { Location } from '@angular/common';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { AD02Page } from './ad02-page';

describe('AD02Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AD02Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([{ path: 'admin/users', component: AD02Page }]),
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('keeps an unauthenticated screen from sending a protected read or claiming the list is empty', () => {
    const fixture = TestBed.createComponent(AD02Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    expect(root.querySelector('h1')?.textContent).toContain('Quản lý tài khoản người dùng');
    expect(text).toContain('Phiên Admin không còn hiệu lực');
    expect(text).not.toContain('Không tìm thấy tài khoản phù hợp');
    expect(root.querySelectorAll('thead th')).toHaveLength(7);
    http.expectNone('/api/v1/admin/users');
  });

  it('renders the verified UserProfile rows and server pagination after API #68 succeeds', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD02Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/users?page=1');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(
      successEnvelope({
        items: [
          userProfile(17, 'Mai Nguyen', 'mai@example.test', 'MENTOR'),
          ...Array.from({ length: 19 }, (_, index) =>
            userProfile(100 + index, `User ${index + 1}`, `user-${index + 1}@example.test`),
          ),
        ],
        pagination: { page: 1, size: 20, total: 41, total_pages: 3 },
      }),
    );
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Mai Nguyen');
    expect(root.textContent).toContain('mai@example.test');
    expect(root.textContent).toContain('1 / 3');
    expect(root.textContent).toContain('41 tài khoản');
    expect(root.querySelector('a[href="/admin/users/17"]')).not.toBeNull();
  });

  it('sends only source-supported filters when they are applied', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD02Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/users?page=1').flush(
      successEnvelope({
        items: [],
        pagination: { page: 1, size: 20, total: 0, total_pages: 0 },
      }),
    );

    const page = fixture.componentInstance;
    page.setFilter('keyword', 'Mai');
    page.setFilter('role', 'MENTOR');
    page.setFilter('status', 'ACTIVE');
    page.applyFilters({ preventDefault: () => undefined } as Event);
    await fixture.whenStable();

    const request = http.expectOne(
      (candidate) =>
        candidate.url === '/api/v1/admin/users' &&
        candidate.params.get('keyword') === 'Mai' &&
        candidate.params.get('role') === 'MENTOR' &&
        candidate.params.get('status') === 'ACTIVE' &&
        candidate.params.get('page') === '1',
    );
    request.flush(
      successEnvelope({
        items: [],
        pagination: { page: 1, size: 20, total: 0, total_pages: 0 },
      }),
    );
    fixture.detectChanges();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain(
      'Không tìm thấy tài khoản phù hợp',
    );
  });

  it('announces loading and separates a retryable server error from the empty state', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD02Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[role="status"]')?.textContent).toContain(
      'Đang tải danh sách người dùng',
    );
    expect(root.querySelector('.empty-title')).toBeNull();

    http
      .expectOne('/api/v1/admin/users?page=1')
      .flush(
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
    fixture.detectChanges();

    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Study Server không thể tải dữ liệu lúc này.',
    );
    expect(root.querySelector('.empty-title')).toBeNull();
    const retry = root.querySelector<HTMLButtonElement>('.query-state-action');
    expect(retry?.textContent).toContain('Thử lại');
    retry!.click();
    fixture.detectChanges();

    http.expectOne('/api/v1/admin/users?page=1').flush(successEnvelope(emptyUsersPage()));
    fixture.detectChanges();
    expect(root.querySelector('[role="alert"]')).toBeNull();
    expect(root.querySelector('.empty-title')?.textContent).toContain('Chưa có dữ liệu');
  });

  it('recovers from API #68 page validation by returning to page 1 and preserving filters', async () => {
    await signIn();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl(
      '/admin/users?panel=staff&keyword=Mai&page=invalid',
      AD02Page,
    );
    await harness.fixture.whenStable();

    http
      .expectOne(
        (request) =>
          request.url === '/api/v1/admin/users' &&
          request.params.get('keyword') === 'Mai' &&
          request.params.get('page') === 'NaN',
      )
      .flush(
        {
          success: false,
          businessCode: 'DESIGN_VALIDATION_ERROR',
          message: 'Dữ liệu đầu vào không hợp lệ.',
          data: null,
          meta: {
            fieldErrors: [
              { field: 'page', code: 'INT_PARSING', message: 'Input should be a valid integer' },
            ],
          },
          traceId: 'test-trace',
        },
        { status: 422, statusText: 'Unprocessable Entity' },
      );
    harness.fixture.detectChanges();

    const root = harness.fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Tham số trang không hợp lệ',
    );
    root.querySelector<HTMLButtonElement>('.query-state-action')!.click();
    await harness.fixture.whenStable();

    const url = new URL(TestBed.inject(Location).path(), 'http://localhost');
    expect(url.searchParams.get('panel')).toBe('staff');
    expect(url.searchParams.get('keyword')).toBe('Mai');
    expect(url.searchParams.get('page')).toBe('1');
    http
      .expectOne(
        (request) =>
          request.url === '/api/v1/admin/users' &&
          request.params.get('keyword') === 'Mai' &&
          request.params.get('page') === '1',
      )
      .flush(successEnvelope(emptyUsersPage()));
    harness.fixture.detectChanges();
    expect(root.querySelector('[role="alert"]')).toBeNull();
    expect(page.query().page).toBe(1);
  });

  it('hydrates filters from the URL, preserves unrelated query state, and restores state after URL navigation', async () => {
    await signIn();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl(
      '/admin/users?panel=staff&keyword=Mai&role=MENTOR&page=2',
      AD02Page,
    );
    await harness.fixture.whenStable();

    const initial = http.expectOne(
      (request) =>
        request.url === '/api/v1/admin/users' &&
        request.params.get('keyword') === 'Mai' &&
        request.params.get('role') === 'MENTOR' &&
        request.params.get('page') === '2',
    );
    initial.flush(
      successEnvelope({
        items: Array.from({ length: 20 }, (_, index) =>
          userProfile(200 + index, `User ${index + 1}`, `user-${index + 1}@example.test`),
        ),
        pagination: { page: 2, size: 20, total: 45, total_pages: 3 },
      }),
    );
    harness.fixture.detectChanges();

    expect(page.filters()).toEqual({ keyword: 'Mai', role: 'MENTOR', status: '' });
    expect((harness.fixture.nativeElement as HTMLElement).textContent).toContain(
      'Bộ lọc đang áp dụng',
    );
    expect((harness.fixture.nativeElement as HTMLElement).textContent).toContain('MENTOR');

    page.setFilter('status', 'ACTIVE');
    page.applyFilters({ preventDefault: () => undefined } as Event);
    await harness.fixture.whenStable();

    let url = new URL(TestBed.inject(Location).path(), 'http://localhost');
    expect(url.searchParams.get('panel')).toBe('staff');
    expect(url.searchParams.get('keyword')).toBe('Mai');
    expect(url.searchParams.get('role')).toBe('MENTOR');
    expect(url.searchParams.get('status')).toBe('ACTIVE');
    expect(url.searchParams.get('page')).toBe('1');
    const applied = http.expectOne(
      (request) =>
        request.url === '/api/v1/admin/users' &&
        request.params.get('keyword') === 'Mai' &&
        request.params.get('role') === 'MENTOR' &&
        request.params.get('status') === 'ACTIVE' &&
        request.params.get('page') === '1',
    );
    applied.flush(successEnvelope({
      items: Array.from({ length: 20 }, (_, index) =>
        userProfile(300 + index, `Filtered ${index + 1}`, `filtered-${index + 1}@example.test`),
      ),
      pagination: { page: 1, size: 20, total: 45, total_pages: 3 },
    }));
    harness.fixture.detectChanges();

    page.changePage(2);
    await harness.fixture.whenStable();
    expect(
      new URL(TestBed.inject(Location).path(), 'http://localhost').searchParams.get('page'),
    ).toBe('2');
    const secondPage = http.expectOne(
      (request) =>
        request.url === '/api/v1/admin/users' &&
        request.params.get('status') === 'ACTIVE' &&
        request.params.get('page') === '2',
    );
    secondPage.flush(
      successEnvelope({
        items: Array.from({ length: 20 }, (_, index) =>
          userProfile(400 + index, `Page two ${index + 1}`, `page-two-${index + 1}@example.test`),
        ),
        pagination: { page: 2, size: 20, total: 45, total_pages: 3 },
      }),
    );
    harness.fixture.detectChanges();

    await TestBed.inject(Router).navigateByUrl(
      '/admin/users?panel=staff&keyword=Mai&role=MENTOR&status=ACTIVE&page=1',
    );
    await harness.fixture.whenStable();
    url = new URL(TestBed.inject(Location).path(), 'http://localhost');
    expect(url.searchParams.get('page')).toBe('1');
    expect(page.filters().status).toBe('ACTIVE');
    expect(page.query().page).toBe(1);
    const restored = http.expectOne(
      (request) =>
        request.url === '/api/v1/admin/users' &&
        request.params.get('status') === 'ACTIVE' &&
        request.params.get('page') === '1',
    );
    restored.flush(successEnvelope(emptyUsersPage()));
    harness.fixture.detectChanges();

    page.clearFilters();
    await harness.fixture.whenStable();
    url = new URL(TestBed.inject(Location).path(), 'http://localhost');
    expect(url.searchParams.get('panel')).toBe('staff');
    expect(url.searchParams.has('keyword')).toBe(false);
    expect(url.searchParams.has('role')).toBe(false);
    expect(url.searchParams.has('status')).toBe(false);
    expect(url.searchParams.get('page')).toBe('1');
    const cleared = http.expectOne(
      (request) =>
        request.url === '/api/v1/admin/users' &&
        request.params.get('page') === '1' &&
        request.params.get('keyword') === null &&
        request.params.get('role') === null &&
        request.params.get('status') === null,
    );
    cleared.flush(successEnvelope(emptyUsersPage()));
    harness.fixture.detectChanges();
    expect(page.activeFilters()).toEqual([]);
  });

  it('refreshes the current source-supported list query without changing its filters', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD02Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/users?page=1').flush(successEnvelope(emptyUsersPage()));
    fixture.detectChanges();

    const page = fixture.componentInstance;
    page.setFilter('keyword', 'An');
    page.applyFilters({ preventDefault: () => undefined } as Event);
    await fixture.whenStable();
    const filtered = http.expectOne(
      (request) =>
        request.url === '/api/v1/admin/users' &&
        request.params.get('keyword') === 'An' &&
        request.params.get('page') === '1',
    );
    filtered.flush(successEnvelope(emptyUsersPage()));
    fixture.detectChanges();

    const refresh = (fixture.nativeElement as HTMLElement).querySelector<HTMLButtonElement>(
      '.refresh-button',
    );
    expect(refresh).not.toBeNull();
    refresh!.click();
    fixture.detectChanges();

    const refreshed = http.expectOne(
      (request) =>
        request.url === '/api/v1/admin/users' &&
        request.params.get('keyword') === 'An' &&
        request.params.get('page') === '1',
    );
    refreshed.flush(successEnvelope(emptyUsersPage()));
    fixture.detectChanges();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain(
      'Hiển thị 0 trên 0 tài khoản',
    );
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('0 / 0');
  });

  it('keeps unsupported account actions disabled and avoids unsupported policy claims', () => {
    const fixture = TestBed.createComponent(AD02Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';

    expect(root.querySelector<HTMLButtonElement>('.page-action--secondary')?.disabled).toBe(true);
    expect(root.querySelector<HTMLButtonElement>('.page-action--primary')?.disabled).toBe(true);
    expect(text).not.toMatch(/RBAC|nhật ký kiểm toán|health/i);
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

function emptyUsersPage() {
  return { items: [], pagination: { page: 1, size: 20, total: 0, total_pages: 0 } };
}

function userProfile(id: number, fullName: string, email: string, role = 'STUDENT') {
  return {
    id,
    full_name: fullName,
    email,
    role,
    avatar_url: null,
    phone: null,
    status: 'ACTIVE',
    created_at: '2026-01-01T00:00:00Z',
    updated_at: '2026-01-02T00:00:00Z',
  };
}
