import { TestBed } from '@angular/core/testing';
import type { ComponentFixture } from '@angular/core/testing';
import { of } from 'rxjs';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import {
  StudentApiService,
  type NotificationRecord,
  type StudentPage,
} from '../../data/student-api.service';
import { ST26Page } from './st26-page';

const page: StudentPage<NotificationRecord> = {
  items: [
    {
      id: 501,
      title: 'Notification',
      content: 'Notification content',
      is_read: false,
      created_at: '2026-11-17T00:00:00Z',
    },
  ],
  pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
};

function envelope<T>(data: T): ApiEnvelope<T> {
  return { success: true, businessCode: 'OK', message: '', data, meta: {}, traceId: 'test' };
}

describe('ST26Page all and unread filters', () => {
  let fixture: ComponentFixture<ST26Page>;
  let getNotifications: ReturnType<typeof vi.fn>;
  let markNotificationRead: ReturnType<typeof vi.fn>;
  let markAllNotificationsRead: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    getNotifications = vi.fn().mockReturnValue(of(envelope(page)));
    markNotificationRead = vi.fn().mockReturnValue(of(envelope(page)));
    markAllNotificationsRead = vi.fn().mockReturnValue(of(envelope(page)));

    await TestBed.configureTestingModule({
      imports: [ST26Page],
      providers: [
        {
          provide: StudentApiService,
          useValue: { getNotifications, markNotificationRead, markAllNotificationsRead },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(ST26Page);
    fixture.detectChanges();
  });

  it('sends only the declared filter query and page', () => {
    const root = fixture.nativeElement as HTMLElement;

    expect(getNotifications).toHaveBeenNthCalledWith(1, { page: 1 });

    root.querySelector<HTMLButtonElement>('[data-filter="unread"]')!.click();
    fixture.detectChanges();
    expect(getNotifications).toHaveBeenNthCalledWith(2, { unreadOnly: true, page: 1 });
    expect(root.querySelector<HTMLButtonElement>('[data-filter="unread"]')?.getAttribute('aria-pressed')).toBe('true');

    root.querySelector<HTMLButtonElement>('[data-filter="all"]')!.click();
    fixture.detectChanges();
    expect(getNotifications).toHaveBeenNthCalledWith(3, { page: 1 });
    expect(root.querySelector<HTMLButtonElement>('[data-filter="all"]')?.getAttribute('aria-pressed')).toBe('true');
  });

  it('keeps the unread filter after marking one notification read', () => {
    const root = fixture.nativeElement as HTMLElement;
    root.querySelector<HTMLButtonElement>('[data-filter="unread"]')!.click();
    fixture.detectChanges();
    root.querySelector<HTMLButtonElement>('[data-action="mark-read"]')!.click();
    fixture.detectChanges();

    expect(markNotificationRead).toHaveBeenCalledWith('501');
    expect(getNotifications).toHaveBeenLastCalledWith({ unreadOnly: true, page: 1 });
  });

  it('keeps the unread filter after marking all notifications read', () => {
    const root = fixture.nativeElement as HTMLElement;
    root.querySelector<HTMLButtonElement>('[data-filter="unread"]')!.click();
    fixture.detectChanges();
    root.querySelector<HTMLButtonElement>('.api-actions button')!.click();
    fixture.detectChanges();

    expect(markAllNotificationsRead).toHaveBeenCalledTimes(1);
    expect(getNotifications).toHaveBeenLastCalledWith({ unreadOnly: true, page: 1 });
  });
});
