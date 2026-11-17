import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter } from '@angular/router';
import { firstValueFrom, of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../core/http/api-envelope';
import { AD07Page } from './AD07/pages/ad07-page';
import { AD13Page } from './AD13/pages/ad13-page';

describe('Admin detail pages', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    const routeParams = convertToParamMap({ courseId: '42', lessonId: '73' });
    await TestBed.configureTestingModule({
      imports: [AD07Page, AD13Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([]),
        {
          provide: ActivatedRoute,
          useValue: { paramMap: of(routeParams), snapshot: { paramMap: routeParams } },
        },
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('renders API #74 course fields and keeps unsupported course claims/actions unavailable', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD07Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/courses/42');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope({
      items: [{
        id: 42,
        title: 'Biology Foundations',
        description: 'A source-backed course description.',
        thumbnail_url: 'https://media.example.test/biology.png',
        price: '250000',
        status: 'PUBLISHED',
        mentor: { id: 8, full_name: 'An Nguyen', avatar_url: null },
      }],
      pagination: { page: 1, size: 1, total: 1, total_pages: 1 },
    }));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    const courseIdField = Array.from(root.querySelectorAll<HTMLElement>('.field-card')).find(
      (field) => field.querySelector('dt')?.textContent?.trim() === 'ID khóa học',
    );
    expect(courseIdField?.querySelector('dd')?.textContent?.trim()).toBe('42');
    expect(text).not.toContain('Mã khóa học');
    expect(text).toContain('Biology Foundations');
    expect(text).toContain('A source-backed course description.');
    expect(text).toContain('An Nguyen');
    expect(text).toContain('250000');
    expect(text).toContain('PUBLISHED');
    expect(text).toContain('https://media.example.test/biology.png');
    expect(text).toContain('Chưa có dữ liệu chương và bài giảng');
    expect(text).not.toContain('ISO-29990');
    expect(root.querySelectorAll<HTMLButtonElement>('.action-list button').length).toBe(3);
    expect(Array.from(root.querySelectorAll<HTMLButtonElement>('.action-list button')).every((button) => button.disabled)).toBe(true);
  });

  it('renders API #83 lesson fields as text and does not fabricate resource counts or embed media', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD13Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/lessons/73');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope({
      id: 73,
      course_id: 42,
      title: 'Cell Structure',
      content: '<script>alert(1)</script>Read the lesson notes.',
      video_url: 'https://media.example.test/cell.mp4',
      order: 2,
      status: 'ACTIVE',
    }));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    const courseIdField = Array.from(root.querySelectorAll<HTMLElement>('.field-card')).find(
      (field) => field.querySelector('dt')?.textContent?.trim() === 'ID khóa học',
    );
    expect(courseIdField?.querySelector('dd')?.textContent?.trim()).toBe('42');
    expect(text).not.toContain('Mã khóa học');
    expect(text).toContain('Cell Structure');
    expect(text).toContain('<script>alert(1)</script>Read the lesson notes.');
    expect(text).toContain('https://media.example.test/cell.mp4');
    expect(text).toContain('Không có kết quả truy vấn tài nguyên');
    expect(text).not.toContain('0 mục');
    expect(text).not.toContain('0 tệp tin');
    expect(root.querySelector('script')).toBeNull();
    expect(root.querySelector('iframe')).toBeNull();
    expect(root.querySelector<HTMLButtonElement>('.locked-action')?.disabled).toBe(true);
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
