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
    expect(root.querySelector('h1')?.textContent).toContain('Danh sách người dùng');
    expect(text).toContain('Phiên Admin không còn hiệu lực');
    expect(text).not.toContain('Không tìm thấy tài khoản phù hợp');
    expect(root.querySelectorAll('thead th')).toHaveLength(6);
    http.expectNone('/api/v1/admin/users');
  });

  it('renders the verified UserProfile rows and server pagination after API #68 succeeds', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD02Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/users?page=1');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope({
      items: [
        {
          id: 17,
          full_name: 'Mai Nguyen',
          email: 'mai@example.test',
          role: 'MENTOR',
          avatar_url: null,
          phone: null,
          status: 'ACTIVE',
          created_at: '2026-01-01T00:00:00Z',
          updated_at: '2026-01-02T00:00:00Z',
        },
      ],
      pagination: { page: 1, size: 20, total: 41, total_pages: 3 },
    }));
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
    http.expectOne('/api/v1/admin/users?page=1').flush(successEnvelope({
      items: [],
      pagination: { page: 1, size: 20, total: 0, total_pages: 0 },
    }));

    const page = fixture.componentInstance;
    page.setFilter('keyword', 'Mai');
    page.setFilter('role', 'MENTOR');
    page.setFilter('status', 'ACTIVE');
    page.applyFilters({ preventDefault: () => undefined } as Event);
    await fixture.whenStable();

    const request = http.expectOne((candidate) =>
      candidate.url === '/api/v1/admin/users'
      && candidate.params.get('keyword') === 'Mai'
      && candidate.params.get('role') === 'MENTOR'
      && candidate.params.get('status') === 'ACTIVE'
      && candidate.params.get('page') === '1',
    );
    request.flush(successEnvelope({
      items: [],
      pagination: { page: 1, size: 20, total: 0, total_pages: 0 },
    }));
    fixture.detectChanges();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Không tìm thấy tài khoản phù hợp');
  });

  it('hydrates filters from the URL, preserves unrelated query state, and restores state after URL navigation', async () => {
    await signIn();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl(
      '/admin/users?panel=staff&keyword=Mai&role=MENTOR&page=2',
      AD02Page,
    );
    await harness.fixture.whenStable();

    const initial = http.expectOne((request) =>
      request.url === '/api/v1/admin/users'
      && request.params.get('keyword') === 'Mai'
      && request.params.get('role') === 'MENTOR'
      && request.params.get('page') === '2',
    );
    initial.flush(successEnvelope({
      items: [],
      pagination: { page: 2, size: 20, total: 45, total_pages: 3 },
    }));
    harness.fixture.detectChanges();

    expect(page.filters()).toEqual({ keyword: 'Mai', role: 'MENTOR', status: '' });
    expect((harness.fixture.nativeElement as HTMLElement).textContent).toContain('Bộ lọc đang áp dụng');
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
    const applied = http.expectOne((request) =>
      request.url === '/api/v1/admin/users'
      && request.params.get('keyword') === 'Mai'
      && request.params.get('role') === 'MENTOR'
      && request.params.get('status') === 'ACTIVE'
      && request.params.get('page') === '1',
    );
    applied.flush(successEnvelope(emptyUsersPage()));
    harness.fixture.detectChanges();

    page.changePage(2);
    await harness.fixture.whenStable();
    expect(new URL(TestBed.inject(Location).path(), 'http://localhost').searchParams.get('page')).toBe('2');
    const secondPage = http.expectOne((request) =>
      request.url === '/api/v1/admin/users'
      && request.params.get('status') === 'ACTIVE'
      && request.params.get('page') === '2',
    );
    secondPage.flush(successEnvelope({
      items: [],
      pagination: { page: 2, size: 20, total: 45, total_pages: 3 },
    }));
    harness.fixture.detectChanges();

    await TestBed.inject(Router).navigateByUrl(
      '/admin/users?panel=staff&keyword=Mai&role=MENTOR&status=ACTIVE&page=1',
    );
    await harness.fixture.whenStable();
    url = new URL(TestBed.inject(Location).path(), 'http://localhost');
    expect(url.searchParams.get('page')).toBe('1');
    expect(page.filters().status).toBe('ACTIVE');
    expect(page.query().page).toBe(1);
    const restored = http.expectOne((request) =>
      request.url === '/api/v1/admin/users'
      && request.params.get('status') === 'ACTIVE'
      && request.params.get('page') === '1',
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
    const cleared = http.expectOne((request) =>
      request.url === '/api/v1/admin/users'
      && request.params.get('page') === '1'
      && request.params.get('keyword') === null
      && request.params.get('role') === null
      && request.params.get('status') === null,
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
    const filtered = http.expectOne((request) =>
      request.url === '/api/v1/admin/users'
      && request.params.get('keyword') === 'An'
      && request.params.get('page') === '1',
    );
    filtered.flush(successEnvelope(emptyUsersPage()));
    fixture.detectChanges();

    const refresh = (fixture.nativeElement as HTMLElement).querySelector<HTMLButtonElement>('.refresh-button');
    expect(refresh).not.toBeNull();
    refresh!.click();
    fixture.detectChanges();

    const refreshed = http.expectOne((request) =>
      request.url === '/api/v1/admin/users'
      && request.params.get('keyword') === 'An'
      && request.params.get('page') === '1',
    );
    refreshed.flush(successEnvelope(emptyUsersPage()));
    fixture.detectChanges();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Hiển thị 0 trên 0 tài khoản');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('0 / 0');
  });

  it('does not render unsupported account actions or policy claims', () => {
    const fixture = TestBed.createComponent(AD02Page);
    fixture.detectChanges();
    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';

    expect(text).not.toMatch(/Thêm người dùng|Xuất dữ liệu|RBAC|bảo mật|đồng bộ|nhật ký kiểm toán|health/i);
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
