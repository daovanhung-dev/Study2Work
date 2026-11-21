import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, type ParamMap } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AD18Page } from './ad18-page';

describe('AD18Page', () => {
  let http: HttpTestingController;
  let routeParams: BehaviorSubject<ParamMap>;

  beforeEach(async () => {
    routeParams = new BehaviorSubject(convertToParamMap({ quizId: '52' }));
    await TestBed.configureTestingModule({
      imports: [AD18Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([]),
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: routeParams.value }, paramMap: routeParams.asObservable() } },
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('shows the route ID and keeps deletion and audit reason disabled without requesting data', () => {
    const fixture = TestBed.createComponent(AD18Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Mã bài kiểm tra 52');
    expect(root.textContent).toContain('Chưa có dữ liệu xem trước');
    expect(root.textContent).toContain('lượt làm bài và câu trả lời');
    expect(root.textContent).toContain('Chưa có yêu cầu xóa nào được gửi');
    expect(root.querySelector('textarea')?.disabled).toBe(true);
    expect(root.querySelector<HTMLButtonElement>('.confirm-action button')?.disabled).toBe(true);
    expect(root.querySelector<HTMLButtonElement>('.confirm-action button')?.getAttribute('aria-disabled')).toBe('true');
    expect(root.querySelector('a[href="/admin/quizzes"]')).not.toBeNull();
    http.expectNone((request) => request.method === 'DELETE' || request.url.includes('/admin/quizzes/'));
  });

  it('preserves int64 route IDs as text when route parameters change', () => {
    const fixture = TestBed.createComponent(AD18Page);
    fixture.detectChanges();

    routeParams.next(convertToParamMap({ quizId: '9007199254740993' }));
    fixture.detectChanges();

    expect((fixture.nativeElement as HTMLElement).textContent).toContain('9007199254740993');
    http.expectNone((request) => request.url.includes('/admin/quizzes/'));
  });
});
