import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import type { StudentPage } from '../../shared/models/student-api.models';
import type { StudentCourseSummary, StudentAchievement, StudentNotification } from '../../shared/models/student-api.models';
import { ST01OverviewService } from '../data-access/st01-overview.service';
import { ST01Page } from './st01-page';

describe('ST01Page', () => {
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
});

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
