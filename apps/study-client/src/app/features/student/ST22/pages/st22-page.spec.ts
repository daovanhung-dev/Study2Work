import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of, throwError } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ST22AchievementsService } from '../data-access/st22-achievements.service';
import type { StudentAchievement, StudentPage } from '../../shared/models/student-api.models';
import { ST22Page } from './st22-page';

describe('ST22Page', () => {
  let achievements: ReturnType<typeof vi.fn>;
  let award: StudentAchievement;

  beforeEach(async () => {
    award = {
      id: 72,
      code: 'COURSE_COMPLETION',
      title: 'Course completed',
      awarded_at: '2026-11-27T09:00:00Z',
      course_id: 12,
    };
    achievements = vi.fn(() => of(apiEnvelope(achievementPage([award]))));

    await TestBed.configureTestingModule({
      imports: [ST22Page],
      providers: [
        provideRouter([{ path: 'student/achievements', component: ST22Page }]),
        { provide: ST22AchievementsService, useValue: { achievements } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('renders returned award fields without inventing certificate actions', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/achievements', ST22Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(achievements).toHaveBeenCalledTimes(1);
    expect(achievements).toHaveBeenCalledWith();
    expect(root.querySelector('.achievement-list h2')?.textContent).toContain(
      'Course completed',
    );
    expect(root.querySelector('.achievement-list .api-meta')?.textContent?.trim()).not.toBe('');
    expect(root.querySelector('.achievement-list a')).toBeNull();
    expect(root.querySelector('.api-muted')?.textContent).toContain(
      'Chứng nhận hiện chưa khả dụng.',
    );
  });

  it('keeps returned awards and offers retry when COUNT and LIST are out of sync', async () => {
    achievements.mockReturnValueOnce(of(apiEnvelope(achievementPage([award], 2))));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/achievements', ST22Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('.achievement-list h2')?.textContent).toContain(
      'Course completed',
    );
    expect(root.querySelector('.achievement-snapshot-warning')?.textContent).toContain(
      'Danh sách và số tổng chưa cập nhật cùng lúc.',
    );
    const retry = root.querySelector<HTMLButtonElement>(
      '.achievement-snapshot-warning button',
    );
    expect(retry).not.toBeNull();
    retry?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(achievements).toHaveBeenCalledTimes(2);
    expect(root.querySelector('.achievement-snapshot-warning')).toBeNull();
    expect(root.querySelector('.api-pill')?.textContent).toContain('1 thành tích');
  });

  it('offers a retry when the achievement request fails', async () => {
    achievements.mockImplementationOnce(() => throwError(() => ({ status: 0 })));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/achievements', ST22Page);
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
    expect(root.querySelector('.achievement-list h2')?.textContent).toContain(
      'Course completed',
    );
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
    traceId: 'st22-test',
  };
}
