import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, type ParamMap } from '@angular/router';
import { BehaviorSubject, firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminContent } from '../../admin-api.models';
import { AD11Page } from './ad11-page';

describe('AD11Page', () => {
  let http: HttpTestingController;
  let routeParams: BehaviorSubject<ParamMap>;

  beforeEach(async () => {
    routeParams = new BehaviorSubject(convertToParamMap({ contentId: '77' }));
    await TestBed.configureTestingModule({
      imports: [AD11Page],
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

  it('loads Content through #79 and renders its supported fields and payload as text', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD11Page);
    fixture.detectChanges();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Đang tải nội dung từ Study Server');
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/content/77');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');

    const item = content({
      payload: {
        html: '<img src=x onerror="alert(1)"><script>alert(1)</script>',
        nested: { label: 'plain text' },
      },
    });
    request.flush(successEnvelope(item));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const metadata = root.querySelector('dl.metadata-grid');
    expect(root.textContent).toContain('Nội dung bài học');
    expect(root.querySelector('nav[aria-label="Đường dẫn kiểm duyệt"]')?.textContent).toContain('Hàng đợi chờ duyệt');
    expect(root.querySelector('nav[aria-label="Đường dẫn kiểm duyệt"]')?.textContent).not.toContain('Hàng chờ chờ duyệt');
    expect(metadata?.textContent).toContain('Mã nội dung');
    expect(metadata?.textContent).toContain('DRAFT');
    expect(metadata?.textContent).not.toContain('Payload');
    expect(root.querySelector('pre')?.textContent).toBe(JSON.stringify(item.payload, null, 2));
    expect(root.querySelector('img, script, iframe, video, audio')).toBeNull();
    http.expectNone((candidate) => candidate.method !== 'GET');
  });

  it('keeps decisions and the reason field disabled without calling #80 or #81', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD11Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/content/77').flush(successEnvelope(content()));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const reason = root.querySelector<HTMLTextAreaElement>('#decision-reason');
    const buttons = [...root.querySelectorAll<HTMLButtonElement>('.decision-panel button')];
    expect(reason?.disabled).toBe(true);
    expect(reason?.placeholder).toContain('gửi cho giảng viên');
    expect(buttons).toHaveLength(2);
    expect(buttons.every((button) => button.disabled)).toBe(true);
    expect(buttons[0]?.textContent).toContain('Phê duyệt nội dung');
    expect(buttons[0]?.textContent).not.toContain('xuất bản');
    expect(root.textContent).toContain('trường này đang bị khóa');
    http.expectNone((candidate) => candidate.method === 'PATCH');
  });

  it('preserves a signed-int64 route ID and does not display rounded Content IDs', async () => {
    await signIn();
    const largeContentId = '9223372036854775807';
    const unsafeNumber = Number(largeContentId);
    routeParams.next(convertToParamMap({ contentId: largeContentId }));

    const fixture = TestBed.createComponent(AD11Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne(`/api/v1/admin/content/${largeContentId}`);
    expect(request.request.method).toBe('GET');
    request.flush(
      successEnvelope(
        content({
          id: unsafeNumber,
          course_id: unsafeNumber,
          parent_id: unsafeNumber,
        }),
      ),
    );
    fixture.detectChanges();

    const fields = [...(fixture.nativeElement as HTMLElement).querySelectorAll('.metadata-item')];
    const valueFor = (label: string) =>
      fields
        .find((field) => field.querySelector('dt')?.textContent?.trim() === label)
        ?.querySelector('dd')
        ?.textContent?.trim();

    expect(valueFor('Mã nội dung')).toBe('Không thể hiển thị chính xác');
    expect(valueFor('Mã khóa học')).toBe('Không thể hiển thị chính xác');
    expect(valueFor('Mã nội dung cha')).toBe('Không thể hiển thị chính xác');
  });

  it('shows the not-found error when #79 returns 404', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD11Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/content/77').flush({
      success: false,
      businessCode: 'DESIGN_RESOURCE_NOT_FOUND',
      message: 'Content not found.',
      data: null,
      meta: {},
      traceId: 'test-trace',
    }, { status: 404, statusText: 'Not Found' });
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent).toContain('Không tìm thấy dữ liệu được yêu cầu.');
    expect(root.querySelector('pre')).toBeNull();
    expect([...root.querySelectorAll<HTMLButtonElement>('.decision-panel button')].every((button) => button.disabled)).toBe(true);
    http.expectNone((candidate) => candidate.method === 'PATCH');
  });

  it('does not call #79 when the route has no content ID', async () => {
    routeParams.next(convertToParamMap({}));
    const fixture = TestBed.createComponent(AD11Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent).toContain('Thiếu mã tham chiếu trên đường dẫn.');
    http.expectNone((candidate) => candidate.url.startsWith('/api/v1/admin/content/'));
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

function content(overrides: Partial<AdminContent> = {}): AdminContent {
  return {
    id: 77,
    course_id: 19,
    content_type: 'LESSON',
    title: 'Nội dung bài học',
    payload: { intro: 'Nội dung xem trước' },
    status: 'DRAFT',
    parent_id: null,
    order: 3,
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
