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
import { GS01Page } from './features/guest/GS01/pages/gs01-page';
import { GS02Page } from './features/guest/GS02/pages/gs02-page';
import { GS03Page } from './features/guest/GS03/pages/gs03-page';
import { GS07Page } from './features/guest/GS07/pages/gs07-page';
import { guestResourceRoutes, guestRoutes } from './features/guest/guest.route';
import { SH01Page } from './features/shared/SH01/pages/sh01-page';
import { SH02Page } from './features/shared/SH02/pages/sh02-page';
import { SH03Page } from './features/shared/SH03/pages/sh03-page';
import { SH04Page } from './features/shared/SH04/pages/sh04-page';
import { SH05Page } from './features/shared/SH05/pages/sh05-page';
import { SH06Page } from './features/shared/SH06/pages/sh06-page';
import { SH07Page } from './features/shared/SH07/pages/sh07-page';
import { sharedRoutes } from './features/shared/shared.route';
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

  it('maps all route-backed Shared and Guest screens to their current page components', () => {
    const sharedChildren = sharedRoutes.find(
      (route) => route.component === SharedLayout,
    )?.children ?? [];
    const sharedScreens = [
      { path: 'forbidden', page: SH05Page },
      { path: 'not-found', page: SH06Page },
      { path: 'operations/:operationId', page: SH07Page },
      { path: '', page: SH01Page },
      { path: 'login', page: SH02Page },
      { path: 'register/verification', page: SH04Page },
      { path: 'register', page: SH03Page },
    ];
    expect(sharedChildren).toHaveLength(sharedScreens.length);
    for (const screen of sharedScreens) {
      const matches = sharedChildren.filter((route) => route.path === screen.path);
      expect(matches).toHaveLength(1);
      expect(matches[0]?.component).toBe(screen.page);
    }

    const guestChildren = guestRoutes.find(
      (route) => route.component === GuestLayout,
    )?.children ?? [];
    const guestScreens = [
      { path: 'search', page: GS02Page },
      { path: ':courseId', page: GS03Page },
      { path: '', page: GS01Page },
    ];
    expect(guestChildren).toHaveLength(guestScreens.length);
    for (const screen of guestScreens) {
      const matches = guestChildren.filter((route) => route.path === screen.path);
      expect(matches).toHaveLength(1);
      expect(matches[0]?.component).toBe(screen.page);
    }

    const resourceChildren = guestResourceRoutes.find(
      (route) => route.component === GuestLayout,
    )?.children ?? [];
    expect(resourceChildren).toHaveLength(1);
    expect(resourceChildren[0]?.component).toBe(GS07Page);
  });

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

  it('routes an invalid GS-07 resource ID to a safe not-found state without calling API #12', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/resources/private-id-9001', GuestLayout);

    const routedRoot = harness.routeNativeElement as HTMLElement;
    expect(routedRoot.querySelector('[data-screen-id="GS07"]')).not.toBeNull();
    expect(routedRoot.querySelector('[role="alert"]')?.textContent).toContain(
      'Không tìm thấy tài liệu',
    );
    expect(routedRoot.textContent).not.toContain('private-id-9001');
    expect(routedRoot.textContent).not.toContain('Khung ứng dụng đã sẵn sàng');
    expect(routedRoot.querySelector('.resource-crumbs a[href="/courses"]')).not.toBeNull();
    http.expectNone((request) => request.url.startsWith('/api/v1/resources/'));
  });

  it('rejects an invalid SH-07 operation ID without calling API #18', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/operations/preview-only', SharedLayout);

    const routedRoot = harness.routeNativeElement as HTMLElement;
    expect(routedRoot.querySelector('[data-screen-id="SH-07"]')).not.toBeNull();
    expect(routedRoot.querySelector('h1')?.textContent).toContain('Theo dõi tác vụ');
    expect(routedRoot.querySelector('[role="alert"]')?.textContent).toContain(
      'Mã tác vụ không hợp lệ hoặc không còn khả dụng.',
    );
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

  it('renders the SH-02 login form at /login without an initial API call', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/login', SharedLayout);

    expect(harness.routeNativeElement?.querySelector('study-sh02-page')).not.toBeNull();
    expect(harness.routeNativeElement?.querySelector('button[type="submit"]')?.hasAttribute('disabled'))
      .toBe(false);
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

  it('sends SH-03 registration to API #01 and explicitly requests SH-04 dispatch through API #02', async () => {
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

    const registrationRoot = harness.routeNativeElement as HTMLElement;
    expect(registrationRoot.querySelector('button.verification-continue')?.textContent)
      .toContain('Tiếp tục yêu cầu xác minh email');
    expect(registrationRoot.textContent).toContain('chưa xác nhận email đã được gửi');
    http.expectNone('/api/v1/auth/verify-email/send');

    registrationRoot.querySelector<HTMLButtonElement>('button.verification-continue')!.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const verificationRoot = harness.routeNativeElement as HTMLElement;
    expect(TestBed.inject(Location).path()).toBe('/register/verification');
    expect(verificationRoot.querySelector('[data-screen-id="SH-04"]')).not.toBeNull();
    expect(verificationRoot.textContent).toContain('Chưa gửi yêu cầu');
    expect(TestBed.inject(Location).path()).not.toContain('1001');
    expect(TestBed.inject(Location).path()).not.toContain('student@example.com');

    verificationRoot.querySelector<HTMLButtonElement>('button.verification-action')!.click();
    const dispatch = http.expectOne('/api/v1/auth/verify-email/send');
    expect(dispatch.request.method).toBe('POST');
    expect(dispatch.request.body).toEqual({ user_id: 1001, email: 'student@example.com' });
    expect(dispatch.request.headers.has('Authorization')).toBe(false);
    dispatch.flush({
      ...successEnvelope({ status: 'accepted' }),
      businessCode: 'DESIGN_OPERATION_ACCEPTED',
    }, { status: 202, statusText: 'Accepted' });
    harness.fixture.detectChanges();

    expect(verificationRoot.textContent).toContain('đã được API #02 chấp nhận');
    expect(verificationRoot.textContent).toContain('Email chưa được gửi thật');
    expect(verificationRoot.textContent).toContain('địa chỉ chưa được xác minh');
  });

  it('renders AD-01 at /admin without the root scaffold', async () => {
    await signInAdmin();
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/admin', AdminLayout);
    await harness.fixture.whenStable();

    const summary = http.expectOne((request) => request.url === '/api/v1/admin/reports/summary');
    expect(summary.request.method).toBe('GET');
    expect(summary.request.headers.get('Authorization')).toBe('Bearer test-access-token');
    expect(summary.request.params.get('from')).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    expect(summary.request.params.get('to')).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    summary.flush({ message: 'report service unavailable' }, {
      status: 503,
      statusText: 'Unavailable',
    });
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

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
    expect(routedRoot.querySelector('h1')?.textContent).toContain('Quản lý tài khoản người dùng');
    expect(routedRoot.querySelector('a[routerLink="/admin/users"]')?.getAttribute('aria-current')).toBe(
      'page',
    );
    expect(routedRoot.querySelector('a[routerLink="/admin"]')?.getAttribute('aria-current')).toBeNull();
    expect(routedRoot.querySelectorAll('tbody .user-record')).toHaveLength(0);
  });

  it('opens the selected AD-03 profile and keeps AD-04/AD-05 actions gated', async () => {
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
    const profileScreen = screen(harness, 'AD03');
    expect(profileScreen.textContent).toContain('Hồ sơ chi tiết tài khoản');
    expect(profileScreen.textContent).toContain('Mã định danh người dùng');
    const editAction = [...profileScreen.querySelectorAll<HTMLButtonElement>('button')]
      .find((button) => button.textContent?.includes('Chỉnh sửa thông tin'));
    const statusAction = [...profileScreen.querySelectorAll<HTMLButtonElement>('button')]
      .find((button) => button.textContent?.includes('Khóa hoặc thay đổi trạng thái'));
    expect(editAction?.disabled).toBe(true);
    expect(statusAction?.disabled).toBe(true);
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
