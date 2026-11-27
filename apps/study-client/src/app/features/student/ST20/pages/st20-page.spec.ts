import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of, throwError } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ST20ProgressService } from '../data-access/st20-progress.service';
import type { StudentAchievement, StudentPage } from '../../shared/models/student-api.models';
import { ST20Page } from './st20-page';

describe('ST20Page', () => {
  let achievements: ReturnType<typeof vi.fn>;
  let award: StudentAchievement;

  beforeEach(async () => {
    award = {
      id: 81,
      code: 'COURSE_COMPLETION',
      title: 'Course completed',
      awarded_at: '2026-11-27T09:00:00Z',
      course_id: 12,
    };
    achievements = vi.fn(() => of(apiEnvelope(achievementPage([award]))));

    await TestBed.configureTestingModule({
      imports: [ST20Page],
      providers: [
        provideRouter([{ path: 'student/progress', component: ST20Page }]),
        { provide: ST20ProgressService, useValue: { achievements } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('keeps aggregate progress unavailable and renders only recorded award details', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/progress', ST20Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const progressGate = root.querySelector('.progress-api-gate');
    expect(achievements).toHaveBeenCalledTimes(1);
    expect(achievements).toHaveBeenCalledWith();
    expect(progressGate?.textContent).toContain('Tiến độ tổng hợp hiện chưa khả dụng.');
    expect(progressGate?.textContent).not.toContain('%');
    expect(progressGate?.querySelector('[role="progressbar"]')).toBeNull();
    expect(root.querySelector('.api-list strong')?.textContent).toContain('Course completed');
    expect(root.querySelector('.api-list .api-meta')?.textContent?.trim()).not.toBe('');
    expect(root.querySelector('.api-list a')).toBeNull();
  });

  it('retains returned award rows and allows retry when COUNT and LIST disagree', async () => {
    achievements.mockReturnValueOnce(of(apiEnvelope(achievementPage([award], 2))));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/progress', ST20Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('.api-list strong')?.textContent).toContain('Course completed');
    expect(root.querySelector('[role="status"]')?.textContent).toContain(
      'Số lượng tổng và bản ghi thành tích chưa khớp',
    );
    const retry = Array.from(root.querySelectorAll('button')).find((button) =>
      button.textContent?.includes('Tải lại thành tích'),
    );
    expect(retry).toBeDefined();
    retry?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(achievements).toHaveBeenCalledTimes(2);
    expect(root.querySelector('[role="status"]')).toBeNull();
    expect(root.querySelector('.api-list strong')?.textContent).toContain('Course completed');
  });

  it('offers a retry when the achievement request fails', async () => {
    achievements.mockImplementationOnce(() => throwError(() => ({ status: 0 })));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/progress', ST20Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')).not.toBeNull();
    const retry = Array.from(root.querySelectorAll('button')).find((button) =>
      button.textContent?.includes('Tải lại thành tích'),
    );
    expect(retry).toBeDefined();
    retry?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(achievements).toHaveBeenCalledTimes(2);
    expect(root.querySelector('[role="alert"]')).toBeNull();
    expect(root.querySelector('.api-list strong')?.textContent).toContain('Course completed');
  });
});

function achievementPage(
  items: StudentAchievement[],
  total = items.length,
): StudentPage<StudentAchievement> {
  return {
    items,
    pagination: {
      page: 1,
      size: Math.max(items.length, 1),
      total,
      total_pages: total > 0 ? 1 : 0,
    },
  };
}

function apiEnvelope<T>(data: T) {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Achievements loaded.',
    data,
    meta: {},
    traceId: 'st20-test',
  };
}
