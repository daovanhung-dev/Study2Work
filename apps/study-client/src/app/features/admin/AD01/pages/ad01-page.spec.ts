import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { Observable, Subject, of, throwError } from 'rxjs';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { AD01ReportService } from '../data-access/ad01-report.service';
import { createAD01DateRange } from '../models/ad01-report.model';
import type { AD01DateRange } from '../models/ad01-report.model';
import { AD01Page } from './ad01-page';

describe('AD01Page', () => {
  let getSummary: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    getSummary = vi.fn((range: AD01DateRange) => of(reportEnvelope(range)));
    await TestBed.configureTestingModule({
      imports: [AD01Page],
      providers: [
        provideRouter([]),
        { provide: AD01ReportService, useValue: { getSummary } },
      ],
    }).compileComponents();
  });

  it('loads the default 30-day period and maps the four API metrics', () => {
    const fixture = TestBed.createComponent(AD01Page);
    fixture.detectChanges();

    expect(getSummary).toHaveBeenCalledWith(createAD01DateRange('last30'));
    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelectorAll('.metric-card')).toHaveLength(4);
    expect(root.textContent).toContain('Tài khoản được tạo');
    expect(root.textContent).toContain('Lượt ghi danh được tạo');
    expect(root.textContent).toContain('Bản ghi thảo luận được tạo');
    expect(Array.from(root.querySelectorAll('.metric-value')).map((node) => node.textContent?.trim())).toEqual([
      '1.200',
      '8',
      '116',
      '31',
    ]);
    expect(root.querySelector('.context-status')?.textContent).toContain('Số liệu đã cập nhật');
    expect(root.querySelector('#services-title')?.textContent).toContain('vận hành máy chủ');
    expect(root.textContent).toContain('Chưa có nguồn trạng thái được kết nối');
  });

  it('uses inclusive Vietnam calendar dates for today, seven days and thirty days', () => {
    const now = new Date('2026-11-21T17:30:00.000Z');

    expect(createAD01DateRange('today', now)).toEqual({ from: '2026-11-22', to: '2026-11-22' });
    expect(createAD01DateRange('last7', now)).toEqual({ from: '2026-11-16', to: '2026-11-22' });
    expect(createAD01DateRange('last30', now)).toEqual({ from: '2026-10-24', to: '2026-11-22' });
  });

  it('requests the selected period and refreshes the same period on demand', () => {
    const fixture = TestBed.createComponent(AD01Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;

    root.querySelector<HTMLButtonElement>('[aria-label="Khoảng thời gian báo cáo"] button:nth-child(2)')?.click();
    fixture.detectChanges();
    expect(getSummary).toHaveBeenLastCalledWith(createAD01DateRange('last7'));

    root.querySelector<HTMLButtonElement>('.refresh-button')?.click();
    fixture.detectChanges();
    expect(getSummary).toHaveBeenCalledTimes(3);
    expect(getSummary).toHaveBeenLastCalledWith(createAD01DateRange('last7'));
  });

  it('shows loading until the API response arrives', () => {
    const pendingResponse = new Subject<ApiEnvelope<unknown>>();
    getSummary.mockImplementation(() => pendingResponse as Observable<ApiEnvelope<unknown>>);
    const fixture = TestBed.createComponent(AD01Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('.context-status')?.textContent).toContain('Đang tải số liệu');
    expect(Array.from(root.querySelectorAll('.metric-value')).every((node) => node.textContent?.trim() === '— —')).toBe(true);

    pendingResponse.next(reportEnvelope(createAD01DateRange('last30')));
    fixture.detectChanges();
    expect(root.querySelector('.context-status')?.textContent).toContain('Số liệu đã cập nhật');
  });

  it('shows a retryable error and recovers after a successful retry', () => {
    getSummary
      .mockReturnValueOnce(throwError(() => new HttpErrorResponse({ status: 403 })))
      .mockReturnValueOnce(of(reportEnvelope(createAD01DateRange('last30'))));
    const fixture = TestBed.createComponent(AD01Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent).toContain('không có quyền xem báo cáo');
    root.querySelector<HTMLButtonElement>('.report-error button')?.click();
    fixture.detectChanges();

    expect(getSummary).toHaveBeenCalledTimes(2);
    expect(root.querySelector('[role="alert"]')).toBeNull();
    expect(root.querySelector('.context-status')?.textContent).toContain('Số liệu đã cập nhật');
  });

  it('keeps the health and audit controls unavailable and preserves safe shortcuts', () => {
    const fixture = TestBed.createComponent(AD01Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const auditButton = root.querySelector<HTMLButtonElement>('.secondary-button');
    expect(auditButton?.disabled).toBe(true);
    expect(Array.from(root.querySelectorAll('.service-state')).every((state) => state.textContent?.trim() === 'Chưa khả dụng')).toBe(true);
    const shortcuts = Array.from(root.querySelectorAll<HTMLAnchorElement>('.shortcut-card[href]'));
    expect(shortcuts.map((link) => link.getAttribute('href'))).toEqual([
      '/admin/users',
      '/admin/courses',
      '/admin/content/pending',
    ]);
  });
});

function reportEnvelope(period: AD01DateRange): ApiEnvelope<unknown> {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Report summary retrieved.',
    data: {
      period,
      metrics: [
        { key: 'user_records_created', value: '1200', label: 'Tài khoản được tạo' },
        { key: 'course_records_created', value: '8', label: 'Khóa học được tạo' },
        { key: 'enrollment_records_created', value: '116', label: 'Lượt ghi danh được tạo' },
        { key: 'discussion_records_created', value: '31', label: 'Bản ghi thảo luận được tạo' },
      ],
      generated_at: '2026-11-22T00:00:00Z',
    },
    meta: {},
    traceId: '00000000-0000-4000-8000-000000000000',
  };
}
