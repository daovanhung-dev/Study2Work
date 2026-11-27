import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { Subject, of } from 'rxjs';
import { afterEach, describe, expect, it, vi } from 'vitest';

import type { StudentPage } from '../../shared/models/student-api.models';
import type { StudentCourseSummary, StudentAchievement, StudentNotification } from '../../shared/models/student-api.models';
import { ST01OverviewService } from '../data-access/st01-overview.service';
import { ST01Page } from './st01-page';

describe('ST01Page', () => {
  afterEach(() => TestBed.resetTestingModule());

  it('renders only validated active-course, achievement and unread-notification data', async () => {
    const data = {
      activeCourses: vi.fn(() => of(envelope(page([course], 20, 1)))),
      achievements: vi.fn(() => of(envelope(page([achievement], 1, 1)))),
      unreadNotifications: vi.fn(() => of(envelope(page([notification], 20, 1)))),
    };
    await TestBed.configureTestingModule({
      imports: [ST01Page],
      providers: [provideRouter([]), { provide: ST01OverviewService, useValue: data }],
    }).compileComponents();

    const fixture = TestBed.createComponent(ST01Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[data-screen-id="ST-01"]')).not.toBeNull();
    expect(root.textContent).toContain('Khóa học đang học');
    expect(root.textContent).toContain('Lập trình Web');
    expect(root.textContent).toContain('Học tập đều đặn');
    expect(root.textContent).toContain('Lịch học tuần này');
    expect(root.textContent).toContain('1');
    expect(data.activeCourses).toHaveBeenCalledOnce();
    expect(data.achievements).toHaveBeenCalledOnce();
    expect(data.unreadNotifications).toHaveBeenCalledOnce();
  });

  it('announces independent API errors and retries only the selected widget', async () => {
    const courseFailure = new Subject<unknown>();
    const achievementFailure = new Subject<unknown>();
    const notificationFailure = new Subject<unknown>();
    const data = {
      activeCourses: vi
        .fn()
        .mockReturnValueOnce(courseFailure)
        .mockReturnValueOnce(of(envelope(page([course], 20, 1)))),
      achievements: vi
        .fn()
        .mockReturnValueOnce(achievementFailure)
        .mockReturnValueOnce(of(envelope(page([achievement], 1, 1)))),
      unreadNotifications: vi
        .fn()
        .mockReturnValueOnce(notificationFailure)
        .mockReturnValueOnce(of(envelope(page([notification], 20, 1)))),
    };

    await TestBed.configureTestingModule({
      imports: [ST01Page],
      providers: [provideRouter([]), { provide: ST01OverviewService, useValue: data }],
    }).compileComponents();

    const fixture = TestBed.createComponent(ST01Page);
    fixture.detectChanges();
    courseFailure.error(new Error('Course request failed.'));
    achievementFailure.error(new Error('Achievement request failed.'));
    notificationFailure.error(new Error('Notification request failed.'));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const courseWidget = findWidget(root, 'overview-courses-title');
    const achievementWidget = findWidget(root, 'overview-achievements-title');
    const notificationWidget = findWidget(root, 'overview-notifications-title');

    expectAlertAndRetry(courseWidget, 'Thử tải lại khóa học');
    expectAlertAndRetry(achievementWidget, 'Thử tải lại thành tích');
    expectAlertAndRetry(notificationWidget, 'Thử tải lại');
    expect(root.querySelectorAll('[role="alert"]')).toHaveLength(3);

    findButton(courseWidget, 'Thử tải lại khóa học').click();
    fixture.detectChanges();

    expect(data.activeCourses).toHaveBeenCalledTimes(2);
    expect(data.achievements).toHaveBeenCalledOnce();
    expect(data.unreadNotifications).toHaveBeenCalledOnce();
    expect(courseWidget.querySelector('[role="alert"]')).toBeNull();
    expect(courseWidget.textContent).toContain('Lập trình Web');
    expect(achievementWidget.querySelector('[role="alert"]')).not.toBeNull();
    expect(notificationWidget.querySelector('[role="alert"]')).not.toBeNull();

    findButton(achievementWidget, 'Thử tải lại thành tích').click();
    fixture.detectChanges();

    expect(data.activeCourses).toHaveBeenCalledTimes(2);
    expect(data.achievements).toHaveBeenCalledTimes(2);
    expect(data.unreadNotifications).toHaveBeenCalledOnce();
    expect(achievementWidget.querySelector('[role="alert"]')).toBeNull();
    expect(achievementWidget.textContent).toContain('Học tập đều đặn');
    expect(notificationWidget.querySelector('[role="alert"]')).not.toBeNull();

    findButton(notificationWidget, 'Thử tải lại').click();
    fixture.detectChanges();

    expect(data.activeCourses).toHaveBeenCalledTimes(2);
    expect(data.achievements).toHaveBeenCalledTimes(2);
    expect(data.unreadNotifications).toHaveBeenCalledTimes(2);
    expect(notificationWidget.querySelector('[role="alert"]')).toBeNull();
    expect(notificationWidget.textContent).toContain('Lịch học tuần này');
  });
});

function findWidget(root: HTMLElement, headingId: string): HTMLElement {
  const widget = root.querySelector(`[aria-labelledby="${headingId}"]`);
  if (!(widget instanceof HTMLElement)) throw new Error(`ST-01 widget ${headingId} is missing.`);
  return widget;
}

function expectAlertAndRetry(widget: HTMLElement, retryLabel: string): void {
  const alert = widget.querySelector('[role="alert"]');
  expect(alert?.textContent?.trim()).toBeTruthy();
  expect(findButton(widget, retryLabel)).toBeInstanceOf(HTMLButtonElement);
}

function findButton(root: HTMLElement, label: string): HTMLButtonElement {
  const button = Array.from(root.querySelectorAll('button')).find((candidate) =>
    candidate.textContent?.includes(label),
  );
  if (!(button instanceof HTMLButtonElement)) throw new Error(`ST-01 button ${label} is missing.`);
  return button;
}

const course: StudentCourseSummary = {
  course_id: 42,
  name: 'Lập trình Web',
  enrollment_status: 'ACTIVE',
  enrolled_at: '2026-11-20T09:00:00Z',
};

const achievement: StudentAchievement = {
  id: 7,
  code: 'STREAK_3',
  title: 'Học tập đều đặn',
  awarded_at: '2026-11-20T09:00:00Z',
};

const notification: StudentNotification = {
  id: 9,
  title: 'Lịch học tuần này',
  content: 'Lịch học đã được cập nhật.',
  is_read: false,
  created_at: '2026-11-20T09:00:00Z',
};

function page<T>(items: T[], size: number, total: number): StudentPage<T> {
  return {
    items,
    pagination: {
      page: 1,
      size,
      total,
      total_pages: total > 0 ? Math.ceil(total / size) : 0,
    },
  };
}

function envelope<T>(data: T) {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Retrieved.',
    data,
    traceId: 'test-trace',
  };
}
