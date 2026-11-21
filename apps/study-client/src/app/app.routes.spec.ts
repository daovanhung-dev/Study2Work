import { provideHttpClient } from '@angular/common/http';
import { Location } from '@angular/common';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { App } from './app';
import { routes } from './app.routes';
import { AdminSessionService } from './core/auth/admin-session.service';
import type { ApiEnvelope } from './core/http/api-envelope';
import { AD01Page } from './features/admin/AD01/pages/ad01-page';
import { SH01Page } from './features/shared/SH01/pages/sh01-page';
import { AdminLayout } from './layouts/admin/admin-layout';
import { GuestLayout } from './layouts/guest/guest-layout';
import { SharedLayout } from './layouts/shared/shared-layout';

describe('Study app routes', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter(routes)],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('routes unknown URLs to SH-06 without carrying the original path or query', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/unknown/private-resource?token=must-not-be-kept', SharedLayout);
    harness.fixture.detectChanges();

    expect(TestBed.inject(Location).path()).toBe('/not-found');
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain(
      'Không tìm thấy trang hoặc tài nguyên yêu cầu',
    );
  });

  it('routes / to the public SH-01 page and loads its independent public regions', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/', SharedLayout);

    const routedRoot = harness.routeNativeElement as HTMLElement;
    expect(routedRoot.querySelector('study-sh01-page')).not.toBeNull();
    expect(routedRoot.querySelector('[data-screen-id="SH01"]')).not.toBeNull();
    expect(routedRoot.textContent).not.toContain('Khung ứng dụng đã sẵn sàng');

    const categories = http.expectOne('/api/v1/categories');
    const courses = http.expectOne((request) =>
      request.url === '/api/v1/courses'
      && request.params.get('page') === '1'
      && request.params.get('size') === '6',
    );
    expect(categories.request.method).toBe('GET');
    expect(courses.request.method).toBe('GET');
    expect(categories.request.headers.has('Authorization')).toBe(false);
    expect(courses.request.headers.has('Authorization')).toBe(false);
    categories.flush(successEnvelope({
      items: [],
      pagination: { page: 1, size: 0, total: 0, total_pages: 1 },
    }));
    courses.flush(successEnvelope({
      items: [],
      pagination: { page: 1, size: 6, total: 0, total_pages: 0 },
    }));
    harness.fixture.detectChanges();
  });

  it('routes a direct GS-07 URL to the gate notice without exposing its ID or calling API #12', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/resources/private-id-9001', GuestLayout);

    const routedRoot = harness.routeNativeElement as HTMLElement;
    expect(routedRoot.querySelector('[data-screen-id="GS07"]')).not.toBeNull();
    expect(routedRoot.querySelector('[role="status"]')?.textContent).toContain(
      'Chưa thể mở tài nguyên này',
    );
    expect(routedRoot.textContent).not.toContain('private-id-9001');
    expect(routedRoot.textContent).not.toContain('Khung ứng dụng đã sẵn sàng');
    expect(routedRoot.querySelector('main a, main button')).toBeNull();
    http.expectNone((request) => request.url.startsWith('/api/v1/resources/'));
  });

  it('routes a direct SH-07 URL to the unavailable notice without exposing its path segment or calling API #18', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/operations/preview-only', SharedLayout);

    const routedRoot = harness.routeNativeElement as HTMLElement;
    expect(routedRoot.querySelector('[data-screen-id="SH-07"]')).not.toBeNull();
    expect(routedRoot.querySelector('study-sh07-availability-notice')).not.toBeNull();
    expect(routedRoot.querySelector('h1')?.textContent).toContain('Theo dõi tác vụ bất đồng bộ');
    expect(routedRoot.textContent).toContain('Chưa thể hiển thị trạng thái tác vụ');
    expect(routedRoot.textContent).not.toContain('preview-only');
    http.expectNone((request) => request.url.startsWith('/api/v1/operations/'));
  });

  it('sends a trimmed SH-01 search to the existing GS-02 route', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/', SharedLayout);
    http.expectOne('/api/v1/categories').flush(successEnvelope({
      items: [],
      pagination: { page: 1, size: 0, total: 0, total_pages: 1 },
    }));
    http.expectOne((request) => request.url === '/api/v1/courses')
      .flush(successEnvelope({
        items: [],
        pagination: { page: 1, size: 6, total: 0, total_pages: 0 },
      }));
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const input = root.querySelector<HTMLInputElement>('#sh01-search-input')!;
    input.value = '  React / TypeScript  ';
    input.dispatchEvent(new Event('input', { bubbles: true }));
    root.querySelector<HTMLFormElement>('#sh01-search')!
      .dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    await harness.fixture.whenStable();

    const route = new URL(TestBed.inject(Location).path(), 'http://localhost');
    expect(route.pathname).toBe('/courses/search');
    expect(route.searchParams.get('q')).toBe('React / TypeScript');

    const searchRequest = http.expectOne((request) =>
      request.url === '/api/v1/courses/search'
      && request.params.get('q') === 'react / typescript'
      && request.params.get('page') === '1',
    );
    expect(searchRequest.request.headers.has('Authorization')).toBe(false);
    searchRequest.flush(successEnvelope({
      items: [],
      pagination: { page: 1, size: 20, total: 0, total_pages: 0 },
    }));
    harness.fixture.detectChanges();

    expect((harness.routeNativeElement as HTMLElement).querySelector('study-gs02-page')).not.toBeNull();
    expect((harness.routeNativeElement as HTMLElement).textContent).not.toContain(
      'Khung ứng dụng đã sẵn sàng',
    );
  });

  it('routes /courses/search to the public GS-02 screen and requests API #07', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/courses/search?q=react', GuestLayout);

    const request = http.expectOne((candidate) =>
      candidate.url === '/api/v1/courses/search'
      && candidate.params.get('q') === 'react'
      && candidate.params.get('page') === '1',
    );
    expect(request.request.headers.has('Authorization')).toBe(false);
    request.flush(successEnvelope({
      items: [],
      pagination: { page: 1, size: 20, total: 0, total_pages: 0 },
    }));
    harness.fixture.detectChanges();

    const routedRoot = harness.routeNativeElement as HTMLElement;
    expect(routedRoot.querySelector('study-gs02-page')).not.toBeNull();
    expect(routedRoot.querySelector('[data-screen-id="GS02"]')).not.toBeNull();
    expect(routedRoot.textContent).toContain('Không tìm thấy khóa học phù hợp');
    expect(routedRoot.textContent).not.toContain('Khung ứng dụng đã sẵn sàng');
  });

  it('renders the public SH-02 presentation at /login without calling auth APIs', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/login', SharedLayout);

    expect(harness.routeNativeElement?.querySelector('study-sh02-page')).not.toBeNull();
    expect(harness.routeNativeElement?.querySelector('button[type="submit"]')?.hasAttribute('disabled'))
      .toBe(true);
    http.expectNone('/api/v1/auth/login');
    http.expectNone('/api/v1/auth/refresh');
    http.expectNone('/api/v1/users/me');
  });

  it('renders the public SH-03 registration form at /register without an initial API call', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/register', SharedLayout);

    const routedRoot = harness.routeNativeElement as HTMLElement;
    expect(routedRoot.querySelector('study-sh03-page')).not.toBeNull();
    expect(routedRoot.querySelector('h1')?.textContent).toContain('Đăng ký tài khoản học viên');
    expect(routedRoot.querySelector('button[type="submit"]')?.hasAttribute('disabled')).toBe(false);
    expect(routedRoot.querySelector('a[href="/login"]')).not.toBeNull();
    http.expectNone('/api/v1/auth/register');
    http.expectNone('/api/v1/auth/verify-email/send');
  });

  it('lets a registered user open SH-04 without passing personal data or calling API #02', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/register', SharedLayout);
    const registerRoot = harness.routeNativeElement as HTMLElement;
    for (const [selector, value] of [
      ['#register-fullname', 'Nguyen Van A'],
      ['#register-email', 'student@example.com'],
      ['#register-password', 'password'],
    ]) {
      const input = registerRoot.querySelector<HTMLInputElement>(selector);
      expect(input).not.toBeNull();
      input!.value = value;
      input!.dispatchEvent(new Event('input', { bubbles: true }));
    }
    registerRoot.querySelector<HTMLFormElement>('form')!
      .dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    harness.fixture.detectChanges();

    http.expectOne('/api/v1/auth/register').flush({
      ...successEnvelope({
        id: 1001,
        email: 'student@example.com',
      }),
      businessCode: 'DESIGN_RESOURCE_CREATED',
    }, { status: 201, statusText: 'Created' });
    harness.fixture.detectChanges();

    expect((harness.routeNativeElement as HTMLElement)
      .querySelector('a[href="/register/verification"]')).not.toBeNull();
    await clickLink(harness, '/register/verification');

    const verificationRoot = harness.routeNativeElement as HTMLElement;
    expect(TestBed.inject(Location).path()).toBe('/register/verification');
    expect(verificationRoot.querySelector('[data-screen-id="SH-04"]')).not.toBeNull();
    expect(verificationRoot.textContent).toContain('Chưa thể xác minh email');
    expect(TestBed.inject(Location).path()).not.toContain('1001');
    expect(TestBed.inject(Location).path()).not.toContain('student@example.com');
    http.expectNone('/api/v1/auth/verify-email/send');
  });

  it('renders AD-01 at /admin without the root scaffold', async () => {
    await signInAdmin();
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/admin', AdminLayout);

    const routedText = harness.routeNativeElement?.textContent ?? '';
    expect(routedText).toContain('Bảng điều khiển quản trị hệ thống');
    expect(routedText).not.toContain('Khung ứng dụng đã sẵn sàng');
  });

  it('renders AD-02 at /admin/users and marks its navigation link current', async () => {
    await signInAdmin();
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/admin/users', AdminLayout);
    await harness.fixture.whenStable();
    const usersRequest = http.expectOne('/api/v1/admin/users?page=1');
    expect(usersRequest.request.headers.get('Authorization')).toBe('Bearer test-access-token');
    usersRequest.flush(successEnvelope({
      items: [],
      pagination: { page: 1, size: 20, total: 0, total_pages: 0 },
    }));
    harness.fixture.detectChanges();

    const routedRoot = harness.routeNativeElement as HTMLElement;
    expect(routedRoot.querySelector('h1')?.textContent).toContain('Danh sách người dùng');
    expect(routedRoot.querySelector('a[routerLink="/admin/users"]')?.getAttribute('aria-current')).toBe(
      'page',
    );
    expect(routedRoot.querySelector('a[routerLink="/admin"]')?.getAttribute('aria-current')).toBeNull();
    expect(routedRoot.querySelectorAll('tbody .user-record')).toHaveLength(0);
  });

  it('keeps the selected user ID through the AD-02 to AD-05 route links', async () => {
    await signInAdmin();
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/admin/users', AdminLayout);
    await harness.fixture.whenStable();
    const usersRequest = http.expectOne('/api/v1/admin/users?page=1');
    expect(usersRequest.request.method).toBe('GET');
    expect(usersRequest.request.headers.get('Authorization')).toBe('Bearer test-access-token');
    usersRequest.flush(successEnvelope({
      items: [
        {
          id: 77,
          full_name: 'User Name',
          email: 'user@example.test',
          role: 'MENTOR',
          avatar_url: null,
          phone: '0900000000',
          status: 'ACTIVE',
          created_at: '2026-01-01T00:00:00Z',
          updated_at: '2026-11-01T00:00:00Z',
        },
      ],
      pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
    }));
    harness.fixture.detectChanges();

    expect(screen(harness, 'AD02').textContent).toContain('User Name');
    await clickLink(harness, '/admin/users/77');
    await flushUserProfile(harness);
    expect(screen(harness, 'AD03').textContent).toContain('Hồ sơ chi tiết tài khoản');

    await clickLink(harness, '/admin/users/77/edit');
    await flushUserProfile(harness);
    const editScreen = screen(harness, 'AD04');
    expect(editScreen.textContent).toContain('User ID từ đường dẫn: 77');
    const saveButton = [...editScreen.querySelectorAll<HTMLButtonElement>('button')]
      .find((button) => button.textContent?.includes('Lưu thay đổi'));
    expect(saveButton?.disabled).toBe(true);
    expectNoUserMutations();

    await clickLink(harness, '/admin/users/77');
    await flushUserProfile(harness);
    expect(screen(harness, 'AD03').textContent).toContain('Hồ sơ chi tiết tài khoản');

    await clickLink(harness, '/admin/users/77/actions');
    await flushUserProfile(harness);
    const actionsScreen = screen(harness, 'AD05');
    expect(actionsScreen.textContent).toContain('User ID từ đường dẫn: 77');
    const actionButtons = [...actionsScreen.querySelectorAll<HTMLButtonElement>('button')];
    expect(actionButtons).toHaveLength(3);
    expect(actionButtons.every((button) => button.disabled)).toBe(true);
    expect(actionsScreen.querySelector<HTMLTextAreaElement>('textarea')?.disabled).toBe(true);
    expectNoUserMutations();
  });

  it('keeps the root component as a router outlet only', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('router-outlet')).not.toBeNull();
    expect(root.textContent).not.toContain('Khung ứng dụng đã sẵn sàng');
  });

  async function clickLink(harness: RouterTestingHarness, href: string): Promise<void> {
    const root = harness.routeNativeElement as HTMLElement;
    const link = [...root.querySelectorAll<HTMLAnchorElement>('a')]
      .find((candidate) => candidate.getAttribute('href') === href);
    expect(link).toBeDefined();
    link?.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, button: 0 }));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();
  }

  async function flushUserProfile(harness: RouterTestingHarness): Promise<void> {
    const request = http.expectOne('/api/v1/admin/users/77');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer test-access-token');
    request.flush(successEnvelope({
      id: 77,
      full_name: 'User Name',
      email: 'user@example.test',
      role: 'MENTOR',
      avatar_url: null,
      phone: '0900000000',
      status: 'ACTIVE',
      created_at: '2026-01-01T00:00:00Z',
      updated_at: '2026-11-01T00:00:00Z',
    }));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();
  }

  function screen(harness: RouterTestingHarness, screenId: string): HTMLElement {
    const root = harness.routeNativeElement as HTMLElement;
    const page = root.querySelector<HTMLElement>(`[data-screen-id="${screenId}"]`);
    expect(page).not.toBeNull();
    return page as HTMLElement;
  }

  function expectNoUserMutations(): void {
    http.expectNone((request) =>
      request.url.startsWith('/api/v1/admin/users') && request.method !== 'GET',
    );
  }

  async function signInAdmin(): Promise<void> {
    const login = firstValueFrom(
      TestBed.inject(AdminSessionService).login('admin@example.test', 'password'),
    );
    http.expectOne('/api/v1/auth/login').flush(successEnvelope({
      full_name: 'Admin User',
      email: 'admin@example.test',
      role: 'ADMIN',
      access_token: 'test-access-token',
      refresh_token: 'test-refresh-token',
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
