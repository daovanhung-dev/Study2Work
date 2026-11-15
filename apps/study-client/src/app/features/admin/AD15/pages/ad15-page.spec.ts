import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminPage, AdminQuiz } from '../../admin-api.models';
import { AD15Page } from './ad15-page';

describe('AD15Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AD15Page],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('renders only the #87 quiz metadata and keeps count/status claims out of rows', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD15Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/quizzes?page=1');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    expect(request.request.params.keys()).toEqual(['page']);
    request.flush(successEnvelope(page([
      quiz(88, 42, 'Cell Biology Assessment', 30, '70.00'),
    ], 1, 1, 1)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    const headers = root.querySelector('thead')?.textContent ?? '';
    expect(text).toContain('Cell Biology Assessment');
    expect(text).toContain('42');
    expect(text).toContain('30');
    expect(text).toContain('70.00');
    expect(headers).toContain('Mã bài kiểm tra');
    expect(headers).toContain('Điểm đạt');
    expect(headers).not.toContain('Số câu hỏi');
    expect(headers).not.toContain('Trạng thái');
    expect(text).not.toContain('0 câu hỏi');
    expect(root.querySelector('a[href="/admin/quizzes/88/statistics"]')).not.toBeNull();
    expect(root.querySelector('a[href="/admin/quizzes/new"]')).not.toBeNull();
  });

  it('sends the exact course/status keys and preserves the signed-int64 course text', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD15Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/quizzes?page=1').flush(successEnvelope(page([], 1, 0, 0)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const courseInput = root.querySelector<HTMLInputElement>('#quiz-course')!;
    const statusInput = root.querySelector<HTMLInputElement>('#quiz-status')!;
    courseInput.value = '9223372036854775807';
    courseInput.dispatchEvent(new Event('input'));
    statusInput.value = 'ARCHIVED';
    statusInput.dispatchEvent(new Event('input'));
    root.querySelector<HTMLFormElement>('form')!.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/quizzes?course=9223372036854775807&status=ARCHIVED&page=1');
    expect(request.request.params.keys()).toEqual(['course', 'status', 'page']);
    expect(request.request.params.get('course')).toBe('9223372036854775807');
    expect(request.request.params.get('status')).toBe('ARCHIVED');
    request.flush(successEnvelope(page([], 1, 0, 0)));
  });

  it('uses server pagination bounds and displays an actual empty response', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD15Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/quizzes?page=1').flush(successEnvelope(page([], 1, 0, 0)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Không có bài kiểm tra phù hợp');
    expect(root.textContent).toContain('0 bài kiểm tra phù hợp');
    expect(root.querySelector('.pagination-controls')).toBeNull();
  });

  it('loads the next page within the returned pagination range', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD15Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/quizzes?page=1').flush(successEnvelope(page([
      quiz(88, 42, 'Cell Biology Assessment', 30, '70'),
    ], 1, 21, 2)));
    fixture.detectChanges();

    (fixture.nativeElement as HTMLElement).querySelector<HTMLButtonElement>('.pagination-controls button:last-child')!.click();
    fixture.detectChanges();
    await fixture.whenStable();
    const request = http.expectOne('/api/v1/admin/quizzes?page=2');
    request.flush(successEnvelope(page([
      quiz(89, 42, 'Genetics Assessment', 20, '65'),
    ], 2, 21, 2)));
    fixture.detectChanges();

    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Genetics Assessment');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Trang 2 / 2');
  });

  it('does not create a statistics link from an unsafe JavaScript integer', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD15Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/quizzes?page=1').flush(successEnvelope(page([
      quiz(9007199254740992, 42, 'Large quiz ID', 15, '60'),
    ], 1, 1, 1)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('a[href^="/admin/quizzes/"][href$="/statistics"]')).toBeNull();
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

function quiz(id: number, courseId: number, title: string, duration: number | null, passingScore: string): AdminQuiz {
  return {
    id,
    course_id: courseId,
    title,
    duration_minutes: duration,
    passing_score: passingScore,
    questions: [],
  };
}

function page(items: readonly AdminQuiz[], pageNumber: number, total: number, totalPages: number): AdminPage<AdminQuiz> {
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
