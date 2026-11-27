import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of, Subject } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ST16ResultService } from '../data-access/st16-result.service';
import { ST16Page } from './st16-page';

describe('ST16Page', () => {
  let loadResult: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    loadResult = vi.fn();

    await TestBed.configureTestingModule({
      imports: [ST16Page],
      providers: [
        provideRouter([{ path: 'student/attempts/:attemptId/result', component: ST16Page }]),
        { provide: ST16ResultService, useValue: { result: loadResult } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('shows the pending state without a score or answer details', async () => {
    loadResult.mockReturnValue(of(apiEnvelope(attemptData('PENDING_GRADE', null, null))));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/attempts/42/result', ST16Page);

    const root = harness.routeNativeElement as HTMLElement;
    expect(loadResult).toHaveBeenCalledTimes(1);
    expect(loadResult).toHaveBeenCalledWith('42');
    expect(root.textContent).toContain('Đang chờ chấm');
    expect(root.querySelector('.result-score')).toBeNull();
    expect(root.textContent).not.toContain('Điểm số');
    expect(root.textContent).not.toContain('501');
  });

  it('shows the graded score without turning the returned pass value into a claim', async () => {
    loadResult.mockReturnValue(of(apiEnvelope(attemptData('GRADED', '95', true))));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/attempts/42/result', ST16Page);

    const root = harness.routeNativeElement as HTMLElement;
    expect(loadResult).toHaveBeenCalledWith('42');
    expect(root.querySelector('.result-score strong')?.textContent?.trim()).toBe('95');
    expect(root.textContent).toContain('Trạng thái: Đã chấm');
    expect(root.textContent).not.toContain('Đạt');
    expect(root.textContent).not.toContain('Không đạt');
    expect(root.textContent).not.toContain('501');
  });

  it('ignores a stale result after the route changes to another attempt', async () => {
    const staleResult = new Subject<unknown>();
    loadResult.mockImplementation((attemptId: string) =>
      attemptId === '42'
        ? staleResult
        : of(apiEnvelope({ ...attemptData('GRADED', '95', true), id: 43 })),
    );

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/attempts/42/result', ST16Page);
    await harness.navigateByUrl('/student/attempts/43/result', ST16Page);

    const root = harness.routeNativeElement as HTMLElement;
    expect(loadResult).toHaveBeenNthCalledWith(1, '42');
    expect(loadResult).toHaveBeenNthCalledWith(2, '43');
    expect(root.querySelector('.result-score strong')?.textContent?.trim()).toBe('95');

    staleResult.next(apiEnvelope(attemptData('GRADED', '42', true)));
    harness.fixture.detectChanges();

    expect(root.querySelector('.result-score strong')?.textContent?.trim()).toBe('95');
  });

  it('reports an unsupported result status instead of claiming the attempt ID mismatched', async () => {
    loadResult.mockReturnValue(of(apiEnvelope(attemptData('IN_PROGRESS', '100', true))));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/attempts/42/result', ST16Page);

    const root = harness.routeNativeElement as HTMLElement;
    const alert = root.querySelector('[role="alert"]');
    expect(alert?.textContent).toContain('Trạng thái kết quả bài kiểm tra chưa được hỗ trợ.');
    expect(alert?.textContent).not.toContain('không khớp');
    expect(root.querySelector('.result-score')).toBeNull();
    expect(root.querySelector('button')?.textContent).toContain('Tải lại kết quả');
  });

  it('treats a missing result status as unsupported', async () => {
    const data = attemptData('GRADED', '100', true) as Record<string, unknown>;
    delete data['status'];
    loadResult.mockReturnValue(of(apiEnvelope(data)));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/attempts/42/result', ST16Page);

    const root = harness.routeNativeElement as HTMLElement;
    const alert = root.querySelector('[role="alert"]');
    expect(alert?.textContent).toContain('Trạng thái kết quả bài kiểm tra chưa được hỗ trợ.');
    expect(alert?.textContent).not.toContain('không khớp');
    expect(root.querySelector('.result-score')).toBeNull();
  });

  it('uses a safe load error for malformed identity data', async () => {
    loadResult.mockReturnValue(
      of(
        apiEnvelope({
          quiz_id: 7,
          status: 'GRADED',
          started_at: '2026-11-27T03:00:00Z',
          score: '100',
          passed: true,
          answers: [],
        }),
      ),
    );

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/attempts/42/result', ST16Page);

    const root = harness.routeNativeElement as HTMLElement;
    const alert = root.querySelector('[role="alert"]');
    expect(alert?.textContent).toContain('Chưa thể tải kết quả bài kiểm tra.');
    expect(alert?.textContent).not.toContain('không khớp');
    expect(root.querySelector('.result-score')).toBeNull();
  });

  it('keeps the attempt mismatch message for a different returned ID', async () => {
    loadResult.mockReturnValue(of(apiEnvelope({ ...attemptData('GRADED', '100', true), id: 43 })));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/attempts/42/result', ST16Page);

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Kết quả không khớp với bài kiểm tra này.',
    );
    expect(root.querySelector('[role="alert"]')?.textContent).not.toContain('chưa được hỗ trợ');
    expect(root.querySelector('.result-score')).toBeNull();
  });
});

function attemptData(status: string, score: string | null, passed: boolean | null) {
  return {
    id: 42,
    quiz_id: 7,
    status,
    started_at: '2026-11-27T03:00:00Z',
    submitted_at: '2026-11-27T03:05:00Z',
    score,
    passed,
    answers: [{ question_id: 501 }],
  };
}

function apiEnvelope<T>(data: T) {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Attempt result retrieved.',
    data,
    meta: {},
    traceId: 'st16-test',
  };
}
