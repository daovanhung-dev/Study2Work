import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminContent, AdminPage } from '../../admin-api.models';
import { AD10Page } from './ad10-page';

describe('AD10Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AD10Page],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('renders only the #78 content projection and links safely to AD-11', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD10Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/content/pending?page=1');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    expect(request.request.params.keys()).toEqual(['page']);
    request.flush(successEnvelope(page([
      content(73, 42, 'Cell Structure', 'VIDEO', 2),
      content(74, 42, 'Cell Membrane', 'ARTICLE', 3),
    ], 1, 2, 1)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    const headers = root.querySelector('thead')?.textContent ?? '';
    expect(text).toContain('Cell Structure');
    expect(text).toContain('Cell Membrane');
    expect(text).toContain('PENDING_REVIEW');
    expect(text).toContain('42');
    expect(text).toContain('VIDEO');
    expect(text).toContain('ARTICLE');
    expect(text).toContain('2 nội dung phù hợp');
    expect(headers).toContain('Mã nội dung');
    expect(headers).toContain('Mã khóa học');
    expect(headers).toContain('Thứ tự');
    expect(root.querySelector('a[href="/admin/content/73/review"]')).not.toBeNull();
    expect(text).not.toContain('private payload');
    expect(text).not.toContain('Người gửi:');
    expect(text).not.toContain('Thời điểm gửi:');
  });

  it('sends exact type/course query keys and preserves the int64 course value', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD10Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/content/pending?page=1').flush(successEnvelope(page([], 1, 0, 0)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const typeInput = root.querySelector<HTMLInputElement>('#content-type')!;
    const courseInput = root.querySelector<HTMLInputElement>('#course-id')!;
    typeInput.value = 'VIDEO';
    typeInput.dispatchEvent(new Event('input'));
    courseInput.value = '9223372036854775807';
    courseInput.dispatchEvent(new Event('input'));
    root.querySelector<HTMLFormElement>('form')!.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/content/pending?type=VIDEO&course=9223372036854775807&page=1');
    expect(request.request.params.keys()).toEqual(['type', 'course', 'page']);
    expect(request.request.params.get('course')).toBe('9223372036854775807');
    request.flush(successEnvelope(page([], 1, 0, 0)));
  });

  it('uses the response pagination bounds and shows a real empty state', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD10Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/content/pending?page=1').flush(successEnvelope(page([], 1, 0, 0)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Không có nội dung phù hợp');
    expect(root.querySelector('.pagination-controls')).toBeNull();
    expect(root.textContent).toContain('0 nội dung phù hợp');
  });

  it('loads the next page only inside the server pagination range', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD10Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/content/pending?page=1').flush(successEnvelope(contentPage(
      1,
      21,
      content(73, 42, 'Cell Structure', 'VIDEO', 2),
    )));
    fixture.detectChanges();

    (fixture.nativeElement as HTMLElement).querySelector<HTMLButtonElement>('.pagination-controls button:last-child')!.click();
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/content/pending?page=2');
    request.flush(successEnvelope(page([
      content(74, 42, 'Cell Membrane', 'ARTICLE', 3),
    ], 2, 21, 2)));
    fixture.detectChanges();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Trang 2 / 2');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Cell Membrane');
  });

  it('does not create a detail link for an ID outside JavaScript safe integer range', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD10Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/content/pending?page=1').flush(successEnvelope(page([
      content(9007199254740992, 42, 'Large ID content', 'VIDEO', 1),
    ], 1, 1, 1)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('a[href^="/admin/content/"]')).toBeNull();
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

function content(
  id: number,
  courseId: number,
  title: string,
  contentType: string,
  order: number,
): AdminContent {
  return {
    id,
    course_id: courseId,
    content_type: contentType,
    title,
    payload: { body: 'private payload' },
    status: 'PENDING_REVIEW',
    parent_id: null,
    order,
  };
}

function page(items: readonly AdminContent[], pageNumber: number, total: number, totalPages: number): AdminPage<AdminContent> {
  return {
    items,
    pagination: { page: pageNumber, size: 20, total, total_pages: totalPages },
  };
}

function contentPage(pageNumber: number, total: number, firstContent: AdminContent): AdminPage<AdminContent> {
  const offset = (pageNumber - 1) * 20;
  const itemCount = Math.min(20, Math.max(total - offset, 0));
  return page(
    Array.from({ length: itemCount }, (_, index) => index === 0
      ? firstContent
      : content(1000 + offset + index, 42, `Content ${offset + index + 1}`, 'ARTICLE', offset + index + 1)),
    pageNumber,
    total,
    total === 0 ? 0 : Math.ceil(total / 20),
  );
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
