import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, type ParamMap } from '@angular/router';
import { BehaviorSubject, firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminNotification } from '../../admin-api.models';
import { AD21Page } from './ad21-page';

describe('AD21Page', () => {
  let http: HttpTestingController;
  let routeParams: BehaviorSubject<ParamMap>;

  beforeEach(async () => {
    routeParams = new BehaviorSubject(convertToParamMap({ notificationId: '901' }));
    await TestBed.configureTestingModule({
      imports: [AD21Page],
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

  it('renders the #96 status projection and leaves delivery details unavailable', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD21Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/notifications/901/status');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope(notification(901, 'Lịch bảo trì', 'Dịch vụ sẽ tạm dừng lúc 22:00.', ['EMAIL', 'PUSH'], 'QUEUED')));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    expect(root.querySelector('h1')?.textContent?.trim()).toBe('Kiểm soát và giám sát trạng thái thông báo');
    expect(text).toContain('Lịch bảo trì');
    expect(text).toContain('Dịch vụ sẽ tạm dừng lúc 22:00.');
    expect(text).toContain('EMAIL, PUSH');
    expect(text).toContain('QUEUED');
    expect(text).toContain('13/11/2026');
    expect(root.querySelector('.identity-grid')?.textContent).toContain('901');
    expect(root.querySelector('.identity-grid')?.textContent).toContain('Chưa liên kết');
    expect(root.querySelector('.notification-fields')?.textContent).toContain('Không có trong response API #96');
    expect(root.querySelector('.data-boundary')?.textContent).toContain('API không trả người nhận');
    expect(root.querySelector('.aggregate-status .status-badge')?.getAttribute('data-status')).toBe('QUEUED');
    expect(root.querySelector('a[href="/admin/notifications"]')).not.toBeNull();
    expect(text).not.toContain('0 / 0');
    expect(text).not.toContain('In-App');
    expect(text).not.toContain('SMTP');
    expect(text).not.toContain('Delivery count');
    expect(text).not.toContain('Đã đọc');

    const actions = Array.from(root.querySelectorAll<HTMLButtonElement>('.notification-action'));
    expect(actions.map((button) => button.textContent?.replace(/\s+/g, ' ').trim().split('Đang khóa')[0].trim())).toEqual([
      'Cập nhật bản nháp',
      'Hủy bỏ phát hành',
      'Theo dõi qua cổng tác vụ bất đồng bộ (SH-07)',
    ]);
    expect(actions[2].querySelector('.operation-label')?.textContent?.replace(/\s+/g, ' ').trim())
      .toBe('Theo dõi qua cổng tác vụ bất đồng bộ (SH-07)');
    expect(actions[2].querySelector('.operation-status')?.textContent?.trim()).toBe('Đang khóa');
    expect(root.querySelector('.operation-note')?.textContent)
      .toContain('API #18 backend route đã có nhưng client chưa wired handoff/poller cho SH-07');
    expect(actions.every((button) => button.disabled)).toBe(true);
    expect(http.match((candidate) => ['POST', 'PUT', 'PATCH', 'DELETE'].includes(candidate.method))).toHaveLength(0);
  });

  it('preserves the int64 route path as text and suppresses an unsafe ID display', async () => {
    await signIn();
    routeParams.next(convertToParamMap({ notificationId: '9007199254740992' }));
    const fixture = TestBed.createComponent(AD21Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/notifications/9007199254740992/status');
    request.flush(successEnvelope(notification(9007199254740992, 'Thông báo mã lớn', 'Nội dung', ['PUSH'], 'SENT')));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Không thể tải trạng thái thông báo');
    expect(root.textContent).not.toContain('9007199254740992');
    expect(root.querySelector('.status-badge')).toBeNull();
  });

  it('shows the source 404 result when the notification has no status resource', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD21Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/notifications/901/status');
    request.flush({}, { status: 404, statusText: 'Not Found' });
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Không thể tải trạng thái thông báo');
    expect(root.textContent).toContain('Không tìm thấy dữ liệu được yêu cầu.');
    expect(root.querySelector('a[href="/admin/notifications"]')).not.toBeNull();
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

function notification(
  id: number,
  title: string,
  content: string,
  channels: AdminNotification['channels'],
  status: AdminNotification['status'],
): AdminNotification {
  return { id, title, content, channels, status, created_at: '2026-11-13T10:30:00Z' };
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
