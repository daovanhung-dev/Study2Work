import { provideHttpClient } from '@angular/common/http';
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
import { AdminLayout } from './layouts/admin/admin-layout';
import { MentorLayout } from './layouts/mentor/mentor-layout';
import { SystemLayout } from './layouts/system/system-layout';

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

  it('renders the readiness scaffold at the root route', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/', SystemLayout);

    expect(harness.routeNativeElement?.textContent).toContain('Khung ứng dụng đã sẵn sàng');
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
    usersRequest.flush(
      successEnvelope({
        items: [],
        pagination: { page: 1, size: 20, total: 0, total_pages: 0 },
      }),
    );
    harness.fixture.detectChanges();

    const routedRoot = harness.routeNativeElement as HTMLElement;
    expect(routedRoot.querySelector('h1')?.textContent).toContain('Danh sách người dùng');
    expect(
      routedRoot.querySelector('a[routerLink="/admin/users"]')?.getAttribute('aria-current'),
    ).toBe('page');
    expect(
      routedRoot.querySelector('a[routerLink="/admin"]')?.getAttribute('aria-current'),
    ).toBeNull();
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
    usersRequest.flush(
      successEnvelope({
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
      }),
    );
    harness.fixture.detectChanges();

    expect(screen(harness, 'AD02').textContent).toContain('User Name');
    await clickLink(harness, '/admin/users/77');
    await flushUserProfile(harness);
    expect(screen(harness, 'AD03').textContent).toContain('Hồ sơ chi tiết tài khoản');

    await clickLink(harness, '/admin/users/77/edit');
    await flushUserProfile(harness);
    const editScreen = screen(harness, 'AD04');
    expect(editScreen.textContent).toContain('User ID từ đường dẫn: 77');
    const saveButton = [...editScreen.querySelectorAll<HTMLButtonElement>('button')].find(
      (button) => button.textContent?.includes('Lưu thay đổi'),
    );
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

  it('routes Mentor Phase 1 screens (ME-06, ME-07, ME-08) under /mentor', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/mentor/courses/101/content/new', MentorLayout);
    flushPendingRequests();

    const routedText = harness.routeNativeElement?.textContent ?? '';
    expect(routedText).toContain('Tạo nội dung khóa học mới');
  });

  it('routes Mentor Phase 2 screens (ME-09, ME-10) under /mentor/submissions', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/mentor/submissions', MentorLayout);
    flushPendingRequests();
    expect(harness.routeNativeElement?.textContent).toContain('Danh sách bài nộp cần chấm điểm');

    await harness.navigateByUrl('/mentor/submissions/9001', MentorLayout);
    flushPendingRequests();
    expect(harness.routeNativeElement?.textContent).toContain(
      'Đánh giá bài tập và phản hồi học viên',
    );
  });

  it('routes Mentor Phase 3 screens (ME-11, ME-12) under /mentor/support', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/mentor/support', MentorLayout);
    flushPendingRequests();
    expect(harness.routeNativeElement?.textContent).toContain(
      'Hộp thư hỗ trợ và giải đáp thắc mắc học viên',
    );

    await harness.navigateByUrl('/mentor/support/701', MentorLayout);
    flushPendingRequests();
    expect(harness.routeNativeElement?.textContent).toContain(
      'Trao đổi và đóng yêu cầu hỗ trợ học viên',
    );
  });

  it('routes Mentor Phase 4 screens (ME-16, ME-17, ME-18) under /mentor/courses/:courseId', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/mentor/courses/101/progress', MentorLayout);
    flushPendingRequests();
    expect(harness.routeNativeElement?.textContent).toContain('Tiến độ toàn khóa học');

    await harness.navigateByUrl('/mentor/courses/101/students/501/progress', MentorLayout);
    flushPendingRequests();
    expect(harness.routeNativeElement?.textContent).toContain('Tiến độ từng học viên');

    await harness.navigateByUrl('/mentor/courses/101/analytics', MentorLayout);
    flushPendingRequests();
    expect(harness.routeNativeElement?.textContent).toContain('Analytics hoạt động khóa học');
  });

  it('routes Mentor Phase 5 screens (ME-13, ME-14, ME-15) under /mentor/notifications', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/mentor/notifications/recipients', MentorLayout);
    flushPendingRequests();
    expect(harness.routeNativeElement?.textContent).toContain('Chọn người nhận thông báo');

    await harness.navigateByUrl('/mentor/notifications/create?recipients=501', MentorLayout);
    flushPendingRequests();
    expect(harness.routeNativeElement?.textContent).toContain('Tạo và phát hành thông báo');

    await harness.navigateByUrl('/mentor/notifications/status', MentorLayout);
    flushPendingRequests();
    expect(harness.routeNativeElement?.textContent).toContain('Trạng thái gửi thông báo');
  });

  it('keeps the root component as a router outlet only', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('router-outlet')).not.toBeNull();
    expect(root.textContent).not.toContain('Khung ứng dụng đã sẵn sàng');
  });

  function flushPendingRequests(): void {
    const open = http.match(() => true);
    for (const req of open) {
      req.flush(
        successEnvelope({
          items: [],
          pagination: { page: 1, size: 20, total: 0, total_pages: 0 },
        }),
      );
    }
  }

  async function clickLink(harness: RouterTestingHarness, href: string): Promise<void> {
    const root = harness.routeNativeElement as HTMLElement;
    const link = [...root.querySelectorAll<HTMLAnchorElement>('a')].find(
      (candidate) => candidate.getAttribute('href') === href,
    );
    expect(link).toBeDefined();
    link?.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, button: 0 }));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();
  }

  async function flushUserProfile(harness: RouterTestingHarness): Promise<void> {
    const request = http.expectOne('/api/v1/admin/users/77');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer test-access-token');
    request.flush(
      successEnvelope({
        id: 77,
        full_name: 'User Name',
        email: 'user@example.test',
        role: 'MENTOR',
        avatar_url: null,
        phone: '0900000000',
        status: 'ACTIVE',
        created_at: '2026-01-01T00:00:00Z',
        updated_at: '2026-11-01T00:00:00Z',
      }),
    );
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
    http.expectNone(
      (request) => request.url.startsWith('/api/v1/admin/users') && request.method !== 'GET',
    );
  }

  async function signInAdmin(): Promise<void> {
    const login = firstValueFrom(
      TestBed.inject(AdminSessionService).login('admin@example.test', 'password'),
    );
    http.expectOne('/api/v1/auth/login').flush(
      successEnvelope({
        full_name: 'Admin User',
        email: 'admin@example.test',
        role: 'ADMIN',
        access_token: 'test-access-token',
        refresh_token: 'test-refresh-token',
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
