import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, type ParamMap } from '@angular/router';
import { BehaviorSubject, firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminCourse, AdminPage } from '../../admin-api.models';
import { AD08Page } from './ad08-page';

describe('AD08Page', () => {
  let http: HttpTestingController;
  let routeParams: BehaviorSubject<ParamMap>;

  beforeEach(async () => {
    routeParams = new BehaviorSubject(convertToParamMap({ courseId: '9007199254740993' }));
    await TestBed.configureTestingModule({
      imports: [AD08Page],
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

  it('loads the #74 Course projection with the raw int64 route ID and Bearer token', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD08Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/courses/9007199254740993');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope(coursePage(course({ id: 9007199254740992 }))));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Course ID từ đường dẫn: 9007199254740993');
    expect(root.querySelector('label[for="course-id"]')?.textContent).toContain('ID khóa học');
    expect(root.querySelector('label[for="course-id"]')?.textContent).not.toContain('Mã khóa học');
    expect(root.querySelector<HTMLInputElement>('#course-id')?.value).toBe('9007199254740993');
    expect(root.querySelector<HTMLInputElement>('input[name="title"]')?.value).toBe('Course title');
    expect(root.querySelector<HTMLTextAreaElement>('textarea[name="description"]')?.value).toBe('Course description');
    expect(root.querySelector<HTMLInputElement>('input[name="price"]')?.value).toBe('4850000.00');
    expect(root.textContent).toContain('Mentor Example');
    expect(root.textContent).toContain('PUBLISHED');
    expect(root.textContent).toContain('https://media.example.test/course.jpg');
    expect(root.querySelector('img, picture, video, iframe')).toBeNull();
  });

  it('keeps create-like edits local and disables save and thumbnail upload', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD08Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/courses/9007199254740993').flush(successEnvelope(coursePage(course())));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const title = root.querySelector<HTMLInputElement>('input[name="title"]')!;
    title.value = 'Local course title';
    title.dispatchEvent(new Event('input'));
    const description = root.querySelector<HTMLTextAreaElement>('textarea[name="description"]')!;
    description.value = 'Local course description';
    description.dispatchEvent(new Event('input'));
    const price = root.querySelector<HTMLInputElement>('input[name="price"]')!;
    price.value = '4850000.75';
    price.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    expect(fixture.componentInstance.draft()).toEqual({
      title: 'Local course title',
      description: 'Local course description',
      price: '4850000.75',
    });
    expect(root.textContent).toContain('Local course title');
    expect(root.textContent).toContain('Local course description');
    expect(root.querySelectorAll<HTMLButtonElement>('button:disabled')).toHaveLength(2);
    expect(root.querySelector('input[type="file"]')).toBeNull();
    http.expectNone((request) => request.method !== 'GET');
  });

  it('shows an empty-page state when #74 has no course item', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD08Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/courses/9007199254740993').flush(successEnvelope(coursePage()));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('API #74 không trả khóa học cho mã đã yêu cầu.');
    expect(root.querySelector('input[name="title"]')).toBeNull();
    expect(root.querySelector('a[href="/admin/courses"]')).not.toBeNull();
  });

  it('returns to AD-07 using the unchanged route ID and does not call update', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD08Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/courses/9007199254740993').flush(successEnvelope(coursePage(course())));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelectorAll('a[href="/admin/courses/9007199254740993"]')).toHaveLength(2);
    expect(root.textContent).toContain('PUT chưa được client gọi');
    expect([...root.querySelectorAll<HTMLButtonElement>('button')].every((button) => button.disabled)).toBe(true);
    http.expectNone((request) => request.method === 'PUT');
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
