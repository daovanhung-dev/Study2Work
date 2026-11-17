import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminDiscussion, AdminPage } from '../../admin-api.models';
import { AD22Page } from './ad22-page';

describe('AD22Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AD22Page],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('renders only the #97 discussion summary and safely escapes returned content', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD22Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/discussions/reported?page=1');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope(page([
      discussion(701, 'Cần xem xét phản ánh này.', '<img src=x onerror=alert(1)> Nội dung report.', 'Nguyễn An', 55, 'ACTIVE'),
    ], 1, 1, 1)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    const headers = root.querySelector('thead')?.textContent ?? '';
    expect(text).toContain('Cần xem xét phản ánh này.');
    expect(text).toContain('<img src=x onerror=alert(1)> Nội dung report.');
    expect(root.querySelector('tbody img')).toBeNull();
    expect(text).toContain('Nguyễn An');
    expect(text).toContain('55');
    expect(text).toContain('ACTIVE');
    expect(headers).toContain('Trạng thái thảo luận');
    expect(headers).not.toContain('Số report');
    expect(headers).not.toContain('Lý do báo cáo');
    expect(text).toContain('1 thảo luận trong kết quả API #97');
    expect(text).toContain('Response chưa có thông tin của từng report.');
    expect(text).not.toContain('report đang mở');
    expect(root.querySelector('a[href="/admin/discussions/701/moderate"]')).not.toBeNull();
    expect(root.querySelector<HTMLInputElement>('#discussion-search')?.disabled).toBe(true);
  });

  it('sends exact reason and severity filters without adding unsupported keyword search', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD22Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/discussions/reported?page=1').flush(successEnvelope(page([], 1, 0, 0)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const reason = root.querySelector<HTMLInputElement>('#discussion-reason')!;
    const severity = root.querySelector<HTMLInputElement>('#discussion-severity')!;
    reason.value = 'SPAM';
    reason.dispatchEvent(new Event('input'));
    severity.value = 'HIGH';
    severity.dispatchEvent(new Event('input'));
    root.querySelector<HTMLFormElement>('form')!.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/discussions/reported?reason=SPAM&severity=HIGH&page=1');
    expect(request.request.params.keys()).toEqual(['reason', 'severity', 'page']);
    expect(request.request.params.get('reason')).toBe('SPAM');
    expect(request.request.params.get('severity')).toBe('HIGH');
    expect(request.request.params.has('search')).toBe(false);
    request.flush(successEnvelope(page([], 1, 0, 0)));
  });

  it('loads a valid next page within returned pagination metadata', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD22Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/discussions/reported?page=1').flush(successEnvelope(page([
      discussion(701, 'Nội dung đầu', 'Nội dung đầu', 'Nguyễn An', 55, 'ACTIVE'),
    ], 1, 21, 2)));
    fixture.detectChanges();

    (fixture.nativeElement as HTMLElement).querySelector<HTMLButtonElement>('.pagination-controls button:last-child')!.click();
    fixture.detectChanges();
    await fixture.whenStable();
    const request = http.expectOne('/api/v1/admin/discussions/reported?page=2');
    request.flush(successEnvelope(page([
      discussion(702, 'Nội dung trang hai', 'Nội dung trang hai', 'Trần Bình', 56, 'ACTIVE'),
    ], 2, 21, 2)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Nội dung trang hai');
    expect(root.textContent).toContain('Trang 2 / 2');
    expect(root.querySelector<HTMLButtonElement>('.pagination-controls button:last-child')?.disabled).toBe(true);
  });

  it('shows a real empty page and omits pagination controls when there are no reports', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD22Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/discussions/reported?page=1').flush(successEnvelope(page([], 1, 0, 0)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Không có thảo luận phù hợp');
    expect(root.textContent).toContain('0 thảo luận trong kết quả API #97');
    expect(root.querySelector('.pagination-controls')).toBeNull();
  });

  it('does not create an AD-23 route from an unsafe JavaScript integer ID', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD22Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/discussions/reported?page=1').flush(successEnvelope(page([
      discussion(9007199254740992, 'Mã lớn', 'Nội dung', 'Nguyễn An', 55, 'ACTIVE'),
    ], 1, 1, 1)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('a[href^="/admin/discussions/"]')).toBeNull();
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

function discussion(
  id: number,
  title: string,
  content: string,
  fullName: string,
  courseId: number,
  status: string,
): AdminDiscussion {
  return {
    id,
    course_id: courseId,
    title,
    content,
    author: { id: 8, full_name: fullName, avatar_url: null },
    status,
    comments: [],
  };
}

function page(items: readonly AdminDiscussion[], pageNumber: number, total: number, totalPages: number): AdminPage<AdminDiscussion> {
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
