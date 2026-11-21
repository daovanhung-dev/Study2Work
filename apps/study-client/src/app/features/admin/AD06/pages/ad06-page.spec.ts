import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminCourse } from '../../admin-api.models';
import { AD06ApiService } from '../data-access/ad06-api.service';
import { AD06Page } from './ad06-page';

describe('AD06Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AD06Page],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('renders only the source-backed course projection and pagination', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD06Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/courses?page=1');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope(coursePage(
      1,
      21,
      course(42, 'Biology Foundations', 'A course description.', 'An Nguyen', '250000', 'PUBLISHED'),
    )));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    expect(text).toContain('Biology Foundations');
    expect(text).toContain('A course description.');
    expect(text).toContain('An Nguyen');
    expect(text).toContain('250000');
    expect(text).toContain('PUBLISHED');
    expect(text).toContain('21');
    expect(text).toContain('1 / 2');
    expect(text).toContain('20');
    const detailLink = root.querySelector<HTMLAnchorElement>('a[href="/admin/courses/42"]');
    expect(detailLink?.getAttribute('aria-label')).toBe('Xem chi tiết Biology Foundations');
    expect(text).not.toContain('Chờ kiểm duyệt');
    expect(text).not.toContain('Số bài học');
  });

  it('loads the next page only within API pagination bounds', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD06Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/courses?page=1').flush(successEnvelope(coursePage(
      1,
      21,
      course(42, 'Biology Foundations', null, 'An Nguyen', '250000', 'PUBLISHED'),
    )));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    root.querySelector<HTMLButtonElement>('.pagination-controls button:last-child')!.click();
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/courses?page=2');
    request.flush(successEnvelope(coursePage(
      2,
      21,
      course(63, 'Cell Biology', null, 'An Nguyen', '300000', 'DRAFT'),
    )));
    fixture.detectChanges();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('2 / 2');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Cell Biology');
  });

  it('announces access errors instead of rendering them as an empty result', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD06Page);
    fixture.detectChanges();
    await fixture.whenStable();

    http.expectOne('/api/v1/admin/courses?page=1').flush(
      { success: false, businessCode: 'DESIGN_ACCESS_DENIED' },
      { status: 403, statusText: 'Forbidden' },
    );
    await fixture.whenStable();
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Tài khoản không được phép xem dữ liệu này.',
    );
    expect(root.textContent).not.toContain('Không tìm thấy khóa học');
  });

  it('keeps unsupported search, filters, create and export disabled', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD06Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/courses?page=1').flush(successEnvelope({
      items: [],
      pagination: { page: 1, size: 20, total: 0, total_pages: 0 },
    }));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelectorAll<HTMLInputElement>('.filter-grid input:disabled')).toHaveLength(3);
    expect(Array.from(root.querySelectorAll<HTMLButtonElement>('.catalog-actions button, .filter-actions button')).every((button) => button.disabled)).toBe(true);
    expect(root.querySelector('.filter-summary')?.textContent).toContain('Không có bộ lọc nào được gửi cùng yêu cầu API #73.');
    expect(root.textContent).not.toContain('Tất cả danh mục gốc');
    expect(root.textContent).toContain('Không tìm thấy khóa học');
    expect(root.textContent).not.toContain('đang được đồng bộ');
  });

  it('preserves a signed-int64 mentor query as its original string', async () => {
    await signIn();
    const result = firstValueFrom(TestBed.inject(AD06ApiService).getCourses({
      mentor: '9223372036854775807',
      page: 1,
    }));
    const request = http.expectOne('/api/v1/admin/courses?mentor=9223372036854775807&page=1');
    request.flush(successEnvelope({
      items: [],
      pagination: { page: 1, size: 20, total: 0, total_pages: 0 },
    }));
    await result;
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

function course(
  id: number,
  title: string,
  description: string | null,
  mentorName: string,
  price: string,
  status: string,
): AdminCourse {
  return {
    id,
    title,
    description,
    thumbnail_url: null,
    price,
    status,
    mentor: { id: 8, full_name: mentorName, avatar_url: null },
  };
}

function coursePage(pageNumber: number, total: number, firstCourse?: AdminCourse) {
  const offset = (pageNumber - 1) * 20;
  const itemCount = Math.min(20, Math.max(total - offset, 0));
  return {
    items: Array.from({ length: itemCount }, (_, index) => index === 0 && firstCourse
      ? firstCourse
      : course(
          1000 + offset + index,
          `Course ${offset + index + 1}`,
          null,
          'An Nguyen',
          '0',
          'DRAFT',
        )),
    pagination: {
      page: pageNumber,
      size: 20,
      total,
      total_pages: total === 0 ? 0 : Math.ceil(total / 20),
    },
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
