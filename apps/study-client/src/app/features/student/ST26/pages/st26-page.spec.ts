import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of, throwError } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ST26NotificationsService } from '../data-access/st26-notifications.service';
import type { StudentNotification, StudentPage } from '../../shared/models/student-api.models';
import { ST26Page } from './st26-page';

describe('ST26Page', () => {
  let list: ReturnType<typeof vi.fn>;
  let markRead: ReturnType<typeof vi.fn>;
  let markAllRead: ReturnType<typeof vi.fn>;
  let isRead: boolean;
  let failNextList: boolean;

  beforeEach(async () => {
    isRead = false;
    failNextList = false;
    list = vi.fn((unreadOnly: boolean) => {
      if (!unreadOnly && failNextList) {
        failNextList = false;
        return throwError(() => ({ status: 0 }));
      }
      if (unreadOnly && isRead) return of(apiEnvelope(notificationPage([])));
      return of(apiEnvelope(notificationPage([notification(isRead)])));
    });
    markRead = vi.fn(() => {
      isRead = true;
      return of(apiEnvelope(readNotificationPage(), 'DESIGN_RESOURCE_UPDATED'));
    });
    markAllRead = vi.fn(() => {
      isRead = true;
      return of(apiEnvelope({ updated_count: 1 }, 'DESIGN_RESOURCE_UPDATED'));
    });

    await TestBed.configureTestingModule({
      imports: [ST26Page],
      providers: [
        provideRouter([{ path: 'student/notifications', component: ST26Page }]),
        { provide: ST26NotificationsService, useValue: { list, markRead, markAllRead } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('renders API-backed notifications without deriving a destination from notification text', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/notifications', ST26Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(list).toHaveBeenCalledWith(false, 1);
    expect(list).toHaveBeenCalledWith(true, 1);
    expect(root.querySelector('.notification-item strong')?.textContent).toContain(
      'Course update',
    );
    expect(root.querySelector('.notification-item a')).toBeNull();
  });

  it('marks an unread notification and reloads the list and unread state', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/notifications', ST26Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const markReadButton = root.querySelector<HTMLButtonElement>(
      'button[aria-label="Đánh dấu đã đọc: Course update"]',
    );
    expect(markReadButton).not.toBeNull();
    markReadButton?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(markRead).toHaveBeenCalledExactlyOnceWith('51');
    expect(list).toHaveBeenCalledTimes(4);
    expect(list).toHaveBeenNthCalledWith(3, false, 1);
    expect(list).toHaveBeenNthCalledWith(4, true, 1);
    expect(root.querySelector('.api-success')?.textContent).toContain(
      'Thông báo đã được đánh dấu đã đọc.',
    );
    expect(root.querySelector('.notification-read-label')?.textContent).toContain('Đã đọc');
    expect(root.querySelector('.notification-item button')).toBeNull();
  });

  it('offers a retry when the notification list request fails', async () => {
    failNextList = true;

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/notifications', ST26Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')).not.toBeNull();
    const retry = Array.from(root.querySelectorAll('button')).find((button) =>
      button.textContent?.includes('Tải lại danh sách'),
    );
    expect(retry).toBeDefined();
    retry?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(list).toHaveBeenCalledTimes(3);
    expect(root.querySelector('.notification-item strong')?.textContent).toContain(
      'Course update',
    );
    expect(root.querySelector('[role="alert"]')).toBeNull();
  });

  it('marks all unread notifications and reloads the list and unread state', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/notifications', ST26Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const markAllButton = root.querySelector<HTMLButtonElement>(
      '.notification-heading button',
    );
    expect(markAllButton?.disabled).toBe(false);
    markAllButton?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(markAllRead).toHaveBeenCalledTimes(1);
    expect(markAllRead).toHaveBeenCalledWith();
    expect(list).toHaveBeenCalledTimes(4);
    expect(root.querySelector('.api-success')?.textContent).toContain(
      '1 thông báo đã được đánh dấu đã đọc.',
    );
    expect(root.querySelector('.notification-read-label')?.textContent).toContain('Đã đọc');
  });
});

function notification(read: boolean): StudentNotification {
  return {
    id: 51,
    title: 'Course update',
    content: 'A new lesson is available.',
    is_read: read,
    read_at: read ? '2026-11-27T10:00:00Z' : null,
    created_at: '2026-11-27T09:00:00Z',
  };
}

function notificationPage(items: StudentNotification[]): StudentPage<StudentNotification> {
  return {
    items,
    pagination: {
      page: 1,
      size: 20,
      total: items.length,
      total_pages: items.length > 0 ? 1 : 0,
    },
  };
}

function readNotificationPage(): StudentPage<StudentNotification> {
  return {
    items: [notification(true)],
    pagination: { page: 1, size: 1, total: 1, total_pages: 1 },
  };
}

function apiEnvelope<T>(data: T, businessCode = 'DESIGN_RESOURCE_RETRIEVED') {
  return {
    success: true,
    businessCode,
    message: 'Notifications loaded.',
    data,
    meta: {},
    traceId: 'st26-test',
  };
}
