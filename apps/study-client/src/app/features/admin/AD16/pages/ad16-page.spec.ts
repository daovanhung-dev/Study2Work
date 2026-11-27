import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, type ParamMap } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminCourse } from '../../admin-api.models';
import { AD16Page } from './ad16-page';

describe('AD16Page', () => {
  let http: HttpTestingController;
  let routeParamMap: ParamMap;

  beforeEach(async () => {
    routeParamMap = convertToParamMap({});
    await TestBed.configureTestingModule({
      imports: [AD16Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([]),
        { provide: ActivatedRoute, useFactory: () => ({ snapshot: { paramMap: routeParamMap } }) },
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('shows an actionable session error and does not call a protected API while signed out', () => {
    const fixture = TestBed.createComponent(AD16Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent).toContain('Phiên Admin không còn hiệu lực');
    expect(root.querySelector<HTMLSelectElement>('#quiz-course')?.disabled).toBe(true);
    expect(root.querySelector<HTMLButtonElement>('.button--primary')?.disabled).toBe(true);
    http.expectNone('/api/v1/admin/courses?page=1');
    http.expectNone('/api/v1/admin/quizzes');
  });

  it('loads only exact course options from API #73 and applies page recovery rules', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD16Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/courses?page=1');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope(coursePage(1, 21, course(42, 'Biology Foundations'))));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelectorAll('#quiz-course option')).toHaveLength(21);
    expect(root.querySelector('#quiz-course')?.textContent).toContain('Biology Foundations');
    expect(root.textContent).toContain('Trang 1 / 2');
    expect(root.querySelector<HTMLButtonElement>('.button--add')?.disabled).toBe(false);

    root.querySelector<HTMLButtonElement>('.course-pagination button:last-child')!.click();
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/courses?page=2').flush(successEnvelope(coursePage(
      2,
      21,
      course(63, 'Cell Biology'),
    )));
    fixture.detectChanges();

    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Trang 2 / 2');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Cell Biology');
  });

  it('rejects malformed or count-mismatched #73 pages instead of offering an unsafe course selection', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD16Page);
    fixture.detectChanges();
    await fixture.whenStable();

    http.expectOne('/api/v1/admin/courses?page=1').flush(successEnvelope({
      items: [course(42, 'Biology Foundations')],
      pagination: { page: 1, size: 20, total: 21, total_pages: 2 },
    }));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent).toContain('không khớp contract #73');
    expect(root.querySelector<HTMLSelectElement>('#quiz-course')?.disabled).toBe(true);
    expect(root.querySelector<HTMLButtonElement>('.button--primary')?.disabled).toBe(true);
    expect(root.querySelector('.course-pagination')).toBeNull();
  });

  it('keeps the create draft local until API #88 accepts the exact outer string body', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD16Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/courses?page=1').flush(successEnvelope(coursePage(
      1,
      1,
      course(42, 'Biology Foundations'),
    )));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const select = root.querySelector<HTMLSelectElement>('#quiz-course')!;
    expect(select.required).toBe(true);
    expect(select.value).toBe('');
    select.value = '42';
    select.dispatchEvent(new Event('change', { bubbles: true }));
    setInput(root, 'input[name="title"]', 'Biology review');
    setInput(root, 'input[name="duration"]', '45');
    setInput(root, 'input[name="passingScore"]', '72.50');
    root.querySelector<HTMLButtonElement>('.questions-empty .button--add')!.click();
    fixture.detectChanges();
    setInput(root, '.question-editor input[type="text"]', 'What is a cell?');
    root.querySelector<HTMLButtonElement>('.question-editor .inline-action:not(.inline-action--danger)')!.click();
    fixture.detectChanges();
    setInput(root, '.choice-row input[type="text"]', 'The basic unit of life');
    const correct = root.querySelector<HTMLInputElement>('.choice-row input[type="checkbox"]')!;
    correct.checked = true;
    correct.dispatchEvent(new Event('change', { bubbles: true }));
    fixture.detectChanges();

    root.querySelector<HTMLFormElement>('form')!.dispatchEvent(
      new Event('submit', { bubbles: true, cancelable: true }),
    );
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/quizzes');
    expect(request.request.method).toBe('POST');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    expect(request.request.body).toEqual({
      config: '{"course_id":42,"title":"Biology review","duration_minutes":45,"passing_score":"72.50"}',
      questions: '[{"text":"What is a cell?","type":"SINGLE_CHOICE","choices":[{"text":"The basic unit of life","is_correct":true}]}]',
    });
    request.flush({
      ...successEnvelope({
        id: 95,
        course_id: 42,
        title: 'Biology review',
        duration_minutes: 45,
        passing_score: '72.50',
        questions: [{ id: 51, text: 'What is a cell?', type: 'SINGLE_CHOICE', choices: [] }],
      }),
      businessCode: 'DESIGN_RESOURCE_CREATED',
    }, { status: 201, statusText: 'Created' });
    fixture.detectChanges();

    expect(root.querySelector('[role="status"]')?.textContent).toContain('đã được tạo');
    expect(root.querySelector<HTMLButtonElement>('.button--primary')?.disabled).toBe(true);
    expect(root.querySelector<HTMLInputElement>('input[name="title"]')?.disabled).toBe(true);
    expect(root.querySelector('a[href="/admin/quizzes"]')?.textContent).toContain('Danh sách');
    http.expectNone('/api/v1/admin/quizzes');
  });

  it('requires a title before the source-supported create request', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD16Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/courses?page=1').flush(successEnvelope(coursePage(
      1,
      1,
      course(42, 'Biology Foundations'),
    )));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const select = root.querySelector<HTMLSelectElement>('#quiz-course')!;
    select.value = '42';
    select.dispatchEvent(new Event('change', { bubbles: true }));
    fixture.detectChanges();
    expect(root.querySelector<HTMLInputElement>('input[name="title"]')?.required).toBe(true);

    fixture.componentInstance.saveQuiz(new Event('submit', { cancelable: true }));
    fixture.detectChanges();

    expect(root.querySelector('[role="alert"]')?.textContent).toContain('Hãy nhập tên bài kiểm tra');
    expect(fixture.componentInstance.saveStatus()).toBe('error');
    http.expectNone('/api/v1/admin/quizzes');
  });

  it('locks an unexpected 2xx create response until the quiz list is checked', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD16Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/courses?page=1').flush(successEnvelope(coursePage(
      1,
      1,
      course(42, 'Biology Foundations'),
    )));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const select = root.querySelector<HTMLSelectElement>('#quiz-course')!;
    select.value = '42';
    select.dispatchEvent(new Event('change', { bubbles: true }));
    setInput(root, 'input[name="title"]', 'Biology review');
    setInput(root, 'input[name="passingScore"]', '72.50');
    fixture.detectChanges();
    root.querySelector<HTMLFormElement>('form')!.dispatchEvent(
      new Event('submit', { bubbles: true, cancelable: true }),
    );
    fixture.detectChanges();

    http.expectOne('/api/v1/admin/quizzes').flush({
      ...successEnvelope({
        id: 95,
        course_id: 42,
        title: 'Biology review',
        duration_minutes: null,
        passing_score: '72.50',
        questions: [],
      }),
      businessCode: 'DESIGN_RESOURCE_CREATED',
    }, { status: 200, statusText: 'OK' });
    fixture.detectChanges();

    expect(fixture.componentInstance.saveStatus()).toBe('unconfirmed');
    expect(root.querySelector('[role="alert"]')?.textContent).toContain('HTTP 201');
    expect(root.querySelector<HTMLButtonElement>('.button--primary')?.disabled).toBe(true);
    fixture.componentInstance.saveQuiz(new Event('submit', { cancelable: true }));
    http.expectNone('/api/v1/admin/quizzes');
  });

  it('preserves the raw edit ID and keeps edit mutations blocked without a detail contract', () => {
    routeParamMap = convertToParamMap({ quizId: '9007199254740993' });
    const fixture = TestBed.createComponent(AD16Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Quiz ID từ đường dẫn: 9007199254740993');
    expect(root.textContent).toContain('Chưa thể nạp dữ liệu để chỉnh sửa Quiz này');
    expect(root.querySelector<HTMLInputElement>('input[name="title"]')?.disabled).toBe(true);
    expect(root.querySelector<HTMLInputElement>('input[name="duration"]')?.disabled).toBe(true);
    expect(root.querySelector<HTMLInputElement>('input[name="passingScore"]')?.disabled).toBe(true);
    expect(root.querySelector<HTMLButtonElement>('.button--primary')?.disabled).toBe(true);
    http.expectNone('/api/v1/admin/courses?page=1');
    http.expectNone('/api/v1/admin/quizzes');
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

function setInput(root: HTMLElement, selector: string, value: string): void {
  const input = root.querySelector<HTMLInputElement>(selector);
  if (!input) throw new Error(`Missing ${selector}`);
  input.value = value;
  input.dispatchEvent(new Event('input', { bubbles: true }));
}

function course(id: number, title: string): AdminCourse {
  return {
    id,
    title,
    description: null,
    thumbnail_url: null,
    price: '0',
    status: 'PUBLISHED',
    mentor: { id: 8, full_name: 'An Nguyen', avatar_url: null },
  };
}

function coursePage(pageNumber: number, total: number, firstCourse?: AdminCourse) {
  const offset = (pageNumber - 1) * 20;
  const itemCount = Math.min(20, Math.max(total - offset, 0));
  return {
    items: Array.from({ length: itemCount }, (_, index) => index === 0 && firstCourse
      ? firstCourse
      : course(1000 + offset + index, `Course ${offset + index + 1}`)),
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
