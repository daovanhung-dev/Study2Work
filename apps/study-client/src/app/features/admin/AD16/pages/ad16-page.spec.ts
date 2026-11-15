import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, type ParamMap } from '@angular/router';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

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

  it('renders the create builder with blank configuration and no course options', () => {
    const fixture = TestBed.createComponent(AD16Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('input[name="title"]')?.getAttribute('placeholder')).toContain('Nhập tên bài thi');
    expect(root.querySelector('input[name="duration"]')?.getAttribute('min')).toBeNull();
    expect(root.querySelector('input[name="passingScore"]')?.getAttribute('min')).toBeNull();
    expect(root.querySelectorAll('#quiz-course option')).toHaveLength(1);
    expect(root.querySelector<HTMLSelectElement>('#quiz-course')?.disabled).toBe(true);
    expect(root.textContent).toContain('Danh sách khóa học chưa có nguồn xác nhận');
    http.expectNone((request) => request.url.startsWith('/api/v1/admin/quizzes'));
  });

  it('keeps create inputs in component memory while Add Question and Save remain disabled', () => {
    const fixture = TestBed.createComponent(AD16Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;

    const title = root.querySelector<HTMLInputElement>('input[name="title"]')!;
    title.value = 'Bản nháp trong trang';
    title.dispatchEvent(new Event('input'));
    const duration = root.querySelector<HTMLInputElement>('input[name="duration"]')!;
    duration.value = '45';
    duration.dispatchEvent(new Event('input'));
    const score = root.querySelector<HTMLInputElement>('input[name="passingScore"]')!;
    score.value = '72.50';
    score.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    expect(fixture.componentInstance.titleDraft).toBe('Bản nháp trong trang');
    expect(fixture.componentInstance.durationDraft).toBe('45');
    expect(fixture.componentInstance.passingScoreDraft).toBe('72.50');
    expect([...root.querySelectorAll<HTMLButtonElement>('button')].every((button) => button.disabled)).toBe(true);
    expect(root.textContent).toContain('Chưa có autosave');
    expect(root.querySelector('a[href="/admin/quizzes"]')).not.toBeNull();
    http.expectNone((request) => request.url.startsWith('/api/v1/admin/quizzes'));
  });

  it('preserves the raw edit ID and disables fields that cannot be hydrated', () => {
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
    http.expectNone((request) => request.url.startsWith('/api/v1/admin/quizzes'));
  });

  it('returns to the quiz list and does not expose unsupported question editing', () => {
    const fixture = TestBed.createComponent(AD16Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelectorAll('a[routerLink="/admin/quizzes"]')).toHaveLength(3);
    expect(root.querySelector<HTMLButtonElement>('.button--add')?.disabled).toBe(true);
    expect(root.querySelector('.question-editor, [data-question-editor]')).toBeNull();
    expect(root.textContent).toContain('fallback DERIVED');
    expect(root.textContent).toContain('từ chối Quiz có lịch sử làm bài');
    http.expectNone((request) => request.url.startsWith('/api/v1/admin/quizzes'));
  });
});
