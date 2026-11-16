import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, type ParamMap } from '@angular/router';
import { BehaviorSubject, firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminLesson } from '../../admin-api.models';
import { AD14Page } from './ad14-page';

describe('AD14Page', () => {
  let http: HttpTestingController;
  let routeParams: BehaviorSubject<ParamMap>;

  beforeEach(async () => {
    routeParams = new BehaviorSubject(convertToParamMap({ lessonId: '9007199254740993' }));
    await TestBed.configureTestingModule({
      imports: [AD14Page],
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

  it('loads the exact #83 Lesson projection using the raw int64 route ID', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD14Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/lessons/9007199254740993');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope(lesson({ id: 9007199254740992 })));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Lesson ID: 9007199254740993');
    expect(root.querySelector<HTMLInputElement>('input[name="title"]')?.value).toBe('Lesson title');
    expect(root.querySelector<HTMLTextAreaElement>('textarea[name="content"]')?.value).toBe('Plain text content');
    expect(root.querySelector<HTMLInputElement>('input[name="order"]')?.value).toBe('3');
    expect(root.textContent).toContain('77');
    expect(root.textContent).toContain('PUBLISHED');
    expect(root.textContent).toContain('https://media.example.test/lesson.mp4');
    expect(root.querySelector('video, iframe')).toBeNull();
  });

  it('keeps title, content and order edits local while the update buttons remain disabled', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD14Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/lessons/9007199254740993').flush(successEnvelope(lesson()));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const title = root.querySelector<HTMLInputElement>('input[name="title"]')!;
    title.value = 'Local title draft';
    title.dispatchEvent(new Event('input'));
    const content = root.querySelector<HTMLTextAreaElement>('textarea[name="content"]')!;
    content.value = 'Local content draft';
    content.dispatchEvent(new Event('input'));
    const order = root.querySelector<HTMLInputElement>('input[name="order"]')!;
    order.value = '8';
    order.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    expect(fixture.componentInstance.draft()).toEqual({
      title: 'Local title draft',
      content: 'Local content draft',
      order: '8',
    });
    expect([...root.querySelectorAll<HTMLButtonElement>('button')].every((button) => button.disabled)).toBe(true);
    expect(root.textContent).toContain('chỉ là bản nháp trong trang');
    http.expectNone((request) => request.method !== 'GET');
  });

  it('keeps status and delete actions disabled with the exact source gaps visible', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD14Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/lessons/9007199254740993').flush(successEnvelope(lesson()));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('ARCHIVED');
    expect(root.textContent).toContain('DRAFT/PUBLISHED/SUSPENDED');
    expect(root.textContent).toContain('lesson_progress, resources và lesson_uploads');
    expect(root.textContent).toContain('Response không trả dependency counts');
    expect(root.querySelectorAll<HTMLButtonElement>('button:disabled')).toHaveLength(4);
    http.expectNone((request) => request.method === 'PATCH' || request.method === 'PUT' || request.method === 'DELETE');
  });

  it('shows the #83 not-found state and safe return to AD-12', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD14Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/lessons/9007199254740993').flush({}, { status: 404, statusText: 'Not Found' });
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Không tìm thấy dữ liệu được yêu cầu.');
    expect(root.querySelector('a[href="/admin/lessons"]')).not.toBeNull();
    expect(root.querySelector('input[name="title"]')).toBeNull();
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

function lesson(overrides: Partial<AdminLesson> = {}): AdminLesson {
  return {
    id: 5,
    course_id: 77,
    title: 'Lesson title',
    content: 'Plain text content',
    video_url: 'https://media.example.test/lesson.mp4',
    order: 3,
    status: 'PUBLISHED',
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
