import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, type ParamMap } from '@angular/router';
import { BehaviorSubject, firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminCourse, AdminPage } from '../../admin-api.models';
import { AD09Page } from './ad09-page';

describe('AD09Page', () => {
  let http: HttpTestingController;
  let routeParams: BehaviorSubject<ParamMap>;

  beforeEach(async () => {
    routeParams = new BehaviorSubject(convertToParamMap({ courseId: '9007199254740993' }));
    await TestBed.configureTestingModule({
      imports: [AD09Page],
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

  it('loads only the #74 projection and preserves the raw int64 route ID', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD09Page);
    fixture.detectChanges();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Đang tải khóa học');
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/courses/9007199254740993');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope(coursePage(course())));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Course title');
    expect(root.textContent).toContain('PUBLISHED');
    expect(root.textContent).toContain('Mentor Example');
    expect(root.textContent).toContain('4850000.00');
    expect(root.querySelector('.summary-meta div')?.textContent).toContain('ID khóa học');
    expect(root.querySelector('.summary-meta div')?.textContent).toContain('9007199254740993');
    expect(root.textContent).not.toContain('Mã khóa học trên đường dẫn');
    expect(root.textContent).toContain('Course ID từ đường dẫn: 9007199254740993');
    expect(root.querySelectorAll('a[href="/admin/courses/9007199254740993"]')).toHaveLength(2);
    expect(root.querySelector('img, picture, video, iframe')).toBeNull();
    http.expectNone((candidate) => candidate.method !== 'GET');
  });

  it('keeps status, delete and reason actions disabled without mutation requests', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD09Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/courses/9007199254740993').flush(successEnvelope(coursePage(course())));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const buttons = [...root.querySelectorAll<HTMLButtonElement>('button')];
    expect(buttons.map((button) => button.textContent?.trim())).toEqual([
      'Cập nhật trạng thái',
      'Đánh dấu xóa',
    ]);
    expect(buttons.every((button) => button.disabled)).toBe(true);
    expect(root.querySelector<HTMLTextAreaElement>('textarea')?.disabled).toBe(true);
    expect(root.textContent).toContain('ARCHIVED');
    expect(root.textContent).toContain('Không có bước xem trước dependency');
    http.expectNone((candidate) => candidate.method !== 'GET');
  });

  it('shows the #74 empty-page state and returns to the course list', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD09Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/courses/9007199254740993').flush(successEnvelope(coursePage()));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('API #74 không trả khóa học cho mã đã yêu cầu.');
    expect(root.querySelector('a[href="/admin/courses"]')).not.toBeNull();
    expect(root.querySelector('button')).toBeNull();
  });

  it('shows a safe error state when #74 is forbidden', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD09Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/courses/9007199254740993').flush({}, { status: 403, statusText: 'Forbidden' });
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Không thể tải khóa học');
    expect(root.querySelector('a[href="/admin/courses"]')).not.toBeNull();
    expect(root.querySelector('button')).toBeNull();
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

function course(overrides: Partial<AdminCourse> = {}): AdminCourse {
  return {
    id: 77,
    title: 'Course title',
    description: 'Course description',
    thumbnail_url: 'https://media.example.test/course.jpg',
    price: '4850000.00',
    status: 'PUBLISHED',
    mentor: { id: 91, full_name: 'Mentor Example', avatar_url: null },
    ...overrides,
  };
}

function coursePage(item?: AdminCourse): AdminPage<AdminCourse> {
  return {
    items: item ? [item] : [],
    pagination: { page: 1, size: 1, total: item ? 1 : 0, total_pages: item ? 1 : 0 },
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
