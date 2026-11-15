import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminNotification, AdminPage } from '../../admin-api.models';
import { AD19Page } from './ad19-page';

describe('AD19Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AD19Page],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('renders the #92 delivery-backed projection without inventing recipient or delivery fields', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD19Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/notifications?page=1');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    expect(request.request.params.keys()).toEqual(['page']);
    request.flush(successEnvelope(page([
      notification(901, 'Lịch bảo trì', '<img src=x onerror=alert(1)> Dịch vụ sẽ tạm dừng.', ['EMAIL', 'PUSH'], 'QUEUED'),
    ], 1, 1, 1)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    const headers = root.querySelector('thead')?.textContent ?? '';
    expect(text).toContain('Lịch bảo trì');
    expect(text).toContain('<img src=x onerror=alert(1)> Dịch vụ sẽ tạm dừng.');
    expect(root.querySelector('tbody img')).toBeNull();
    expect(text).toContain('EMAIL, PUSH');
    expect(text).toContain('QUEUED');
    expect(headers).toContain('Nội dung');
    expect(headers).toContain('Ngày tạo');
    expect(headers).not.toContain('Người nhận');
    expect(headers).not.toContain('Số delivery');
    expect(root.querySelector('a[href="/admin/notifications/901"]')).not.toBeNull();
    expect(root.querySelector('a[href="/admin/notifications/new"]')).not.toBeNull();
    expect(root.querySelector<HTMLInputElement>('#notification-search')?.disabled).toBe(true);
  });

  it('sends only the exact source status/channel filters and leaves keyword search disabled', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD19Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/notifications?page=1').flush(successEnvelope(page([], 1, 0, 0)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const status = root.querySelector<HTMLSelectElement>('#notification-status')!;
    const channel = root.querySelector<HTMLSelectElement>('#notification-channel')!;
    status.value = 'FAILED';
    status.dispatchEvent(new Event('change'));
    channel.value = 'PUSH';
    channel.dispatchEvent(new Event('change'));
    root.querySelector<HTMLFormElement>('form')!.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/notifications?status=FAILED&channel=PUSH&page=1');
    expect(request.request.params.keys()).toEqual(['status', 'channel', 'page']);
    expect(request.request.params.get('status')).toBe('FAILED');
    expect(request.request.params.get('channel')).toBe('PUSH');
    expect(request.request.params.has('search')).toBe(false);
    request.flush(successEnvelope(page([], 1, 0, 0)));
  });

  it('uses API pagination bounds and loads a valid next page', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD19Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/notifications?page=1').flush(successEnvelope(page([
      notification(901, 'Thông báo cũ hơn', 'Nội dung', ['EMAIL'], 'SENT'),
    ], 1, 21, 2)));
    fixture.detectChanges();

    (fixture.nativeElement as HTMLElement).querySelector<HTMLButtonElement>('.pagination-controls button:last-child')!.click();
    fixture.detectChanges();
    await fixture.whenStable();
    const request = http.expectOne('/api/v1/admin/notifications?page=2');
    request.flush(successEnvelope(page([
      notification(902, 'Thông báo mới hơn', 'Nội dung trang hai', ['PUSH'], 'FAILED'),
    ], 2, 21, 2)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Thông báo mới hơn');
    expect(root.textContent).toContain('Trang 2 / 2');
    expect(root.querySelector<HTMLButtonElement>('.pagination-controls button:last-child')?.disabled).toBe(true);
  });

  it('shows an empty state for an empty source page', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD19Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/notifications?page=1').flush(successEnvelope(page([], 1, 0, 0)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Không có thông báo phù hợp');
    expect(root.textContent).toContain('0 thông báo có delivery');
    expect(root.querySelector('.pagination-controls')).toBeNull();
  });

  it('does not create a tracking link from an unsafe JavaScript integer ID', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD19Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/notifications?page=1').flush(successEnvelope(page([
      notification(9007199254740992, 'Mã lớn', 'Nội dung', ['EMAIL'], 'SENT'),
    ], 1, 1, 1)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('a[href^="/admin/notifications/"]:not([href$="/new"])')).toBeNull();
    expect(root.textContent).toContain('Không thể hiển thị chính xác');
    expect(root.querySelector<HTMLButtonElement>('.row-action')?.disabled).toBe(true);
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
  return {
    id,
    title,
    content,
    channels,
    status,
    created_at: '2026-11-10T12:00:00Z',
  };
}

function page(
  items: readonly AdminNotification[],
  pageNumber: number,
  total: number,
  totalPages: number,
): AdminPage<AdminNotification> {
  return {
    items,
    pagination: { page: pageNumber, size: 20, total, total_pages: totalPages },
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
