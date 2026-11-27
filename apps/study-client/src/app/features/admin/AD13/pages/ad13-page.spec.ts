import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminLesson } from '../../admin-api.models';
import { AD13Page } from './ad13-page';

describe('AD13Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AD13Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([{ path: 'admin/lessons/:lessonId', component: AD13Page }]),
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('calls API #83 with the route ID and safely renders supported Lesson fields', async () => {
    await signIn();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/admin/lessons/27', AD13Page);
    await harness.fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/lessons/27');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope(lesson(27)));
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement!;
    const fields = root.querySelector('.field-grid')?.textContent ?? '';
    expect(page.viewState().status).toBe('loaded');
    expect(root.querySelector('h1')?.textContent).toContain('Hồ sơ chi tiết bài học quản trị');
    expect(root.querySelector('.sync-status')?.textContent).toContain('Đã tải dữ liệu bài học');
    expect(fields).toContain('Bài học đại số');
    expect(fields).toContain('Mã định danh bài học27');
    expect(fields).toContain('ID khóa học3');
    expect(fields).toContain('Thứ tự trong chương2');
    expect(fields).toContain('Trạng thái phát hànhPUBLISHED');
    expect(fields).toContain('URL video (metadata)https://media.example.test/lesson.mp4');
    expect(root.querySelector('pre')?.textContent).toBe('<img src=x onerror="alert(1)">');
    expect(root.querySelector('pre img')).toBeNull();
    expect(root.textContent).toContain('Không có kết quả truy vấn tài nguyên');
    expect(root.textContent).toContain('Chưa có số liệu tổng hợp');
    expect(root.querySelector('a[href="/admin/lessons"]')).not.toBeNull();
    const action = root.querySelector<HTMLButtonElement>('button.locked-action');
    expect(action?.disabled).toBe(true);
    expect(action?.textContent).toContain('AD-14');
    expect(root.querySelector('a[href="/admin/lessons/27/edit"]')).toBeNull();
  });

  it('rejects a malformed route ID without requesting API #83', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/admin/lessons/not-an-id', AD13Page);
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement!;
    expect(page.viewState().status).toBe('error');
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Mã bài học phải là số nguyên signed 64-bit.',
    );
    expect(root.querySelector('.sync-status')?.textContent).toContain('Chưa tải được dữ liệu');
    http.expectNone('/api/v1/admin/lessons/not-an-id');
    http.expectNone('/api/v1/admin/lessons');
  });

  it('rejects an invalid Lesson projection without rendering untrusted fields', async () => {
    await signIn();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/admin/lessons/27', AD13Page);
    await harness.fixture.whenStable();

    const invalidLesson = { ...lesson(27), course_id: '3' } as unknown as AdminLesson;
    http.expectOne('/api/v1/admin/lessons/27').flush(successEnvelope(invalidLesson));
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement!;
    expect(page.viewState().status).toBe('error');
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'API #83 trả Lesson không hợp lệ.',
    );
    expect(root.querySelector('.field-grid')).toBeNull();
    expect(root.querySelector('pre')).toBeNull();
  });

  it('keeps an HTTP failure separate from a loaded Lesson', async () => {
    await signIn();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/admin/lessons/27', AD13Page);
    await harness.fixture.whenStable();

    http.expectOne('/api/v1/admin/lessons/27').flush(
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
    expect(root.querySelector('.field-grid')).toBeNull();
    expect(root.querySelector('.sync-status')?.textContent).toContain('Chưa tải được dữ liệu');
  });

  it('does not accept a success envelope with a business code other than #83 retrieval', async () => {
    await signIn();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/admin/lessons/27', AD13Page);
    await harness.fixture.whenStable();

    http.expectOne('/api/v1/admin/lessons/27').flush(
      successEnvelope(lesson(27), 'DESIGN_RESOURCE_NOT_FOUND'),
    );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement!;
    expect(page.viewState().status).toBe('error');
    expect(root.querySelector('[role="alert"]')).not.toBeNull();
    expect(root.querySelector('.field-grid')).toBeNull();
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

function lesson(id: number): AdminLesson {
  return {
    id,
    course_id: 3,
    title: 'Bài học đại số',
    content: '<img src=x onerror="alert(1)">',
    video_url: 'https://media.example.test/lesson.mp4',
    order: 2,
    status: 'PUBLISHED',
  };
}
