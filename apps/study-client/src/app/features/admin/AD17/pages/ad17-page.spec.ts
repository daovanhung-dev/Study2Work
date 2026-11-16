import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, type ParamMap } from '@angular/router';
import { BehaviorSubject, firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminQuizStatistics } from '../../admin-api.models';
import { AD17Page } from './ad17-page';

describe('AD17Page', () => {
  let http: HttpTestingController;
  let routeParams: BehaviorSubject<ParamMap>;

  beforeEach(async () => {
    routeParams = new BehaviorSubject(convertToParamMap({ quizId: '44' }));
    await TestBed.configureTestingModule({
      imports: [AD17Page],
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

  it('shows the exact current #91 projection and its catalog contract boundary', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD17Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/quizzes/44/statistics');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope(statistics()));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    expect(text).toContain('Mã bài kiểm tra 44');
    expect(text).toContain('Lượt làm bài120');
    expect(text).toContain('Lượt nộp bài105');
    expect(text).toContain('Lượt đã chấm100');
    expect(text).toContain('Điểm trung bình82.7500');
    expect(text).toContain('Lượt đạt75');
    expect(text).toContain('Tỷ lệ đạt (%)75.000');
    expect(text).toContain('ApiEnvelope<Quiz>');
    expect(text).toContain('không khẳng định metric đã được duyệt');
    expect(root.querySelectorAll('.metric-card')).toHaveLength(6);
    expect(text).not.toContain('Phổ điểm');
    expect(text).not.toContain('Kiểm tra kết nối dữ liệu');
  });

  it('preserves the int64 route as text and never rounds unsafe count fields for display', async () => {
    await signIn();
    routeParams.next(convertToParamMap({ quizId: '9007199254740993' }));
    const fixture = TestBed.createComponent(AD17Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/quizzes/9007199254740993/statistics');
    request.flush(successEnvelope(statistics({
      quiz_id: 9007199254740992,
      attempt_count: 9007199254740992,
      passed_attempt_count: null,
      pass_rate_percent: null,
    })));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Mã bài kiểm tra Không thể hiển thị chính xác');
    expect(root.textContent).toContain('Lượt làm bàiKhông thể hiển thị chính xác');
    expect(root.textContent).toContain('Lượt đạt—');
    expect(root.textContent).toContain('Tỷ lệ đạt (%)—');
  });

  it('shows the API 404 state for an unknown Quiz', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD17Page);
    fixture.detectChanges();
    await fixture.whenStable();

    http.expectOne('/api/v1/admin/quizzes/44/statistics').flush({}, { status: 404, statusText: 'Not Found' });
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Không thể tải thống kê');
    expect(root.textContent).toContain('Không tìm thấy dữ liệu được yêu cầu.');
    expect(root.querySelector('.metric-card')).toBeNull();
  });

  it('keeps null score metrics unavailable when the local source has no graded attempts', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD17Page);
    fixture.detectChanges();
    await fixture.whenStable();

    http.expectOne('/api/v1/admin/quizzes/44/statistics').flush(successEnvelope(statistics({
      attempt_count: 0,
      submitted_attempt_count: 0,
      graded_attempt_count: 0,
      average_score: null,
      passed_attempt_count: null,
      pass_rate_percent: null,
    })));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Lượt làm bài0');
    expect(root.textContent).toContain('Điểm trung bình—');
    expect(root.textContent).toContain('Lượt đạt—');
    expect(root.textContent).toContain('ý nghĩa business của các metric chưa được phê duyệt');
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

function statistics(overrides: Partial<AdminQuizStatistics> = {}): AdminQuizStatistics {
  return {
    quiz_id: 44,
    attempt_count: 120,
    submitted_attempt_count: 105,
    graded_attempt_count: 100,
    average_score: '82.7500',
    passed_attempt_count: 75,
    pass_rate_percent: '75.000',
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
