import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { of, throwError } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { AD20NotificationService } from '../data-access/ad20-notification.service';
import { AD20Page } from './ad20-page';

const operationId = 'cd0ba62a-30df-4b61-9b78-94384a34e70d';

describe('AD20Page', () => {
  it('loads explicit recipients and submits the selected IDs, text and supported channels', async () => {
    const getRecipients = vi.fn((page: number) => of(recipientEnvelope(page)));
    const createNotification = vi.fn(() => of({
      status: 202,
      body: {
        success: true,
        businessCode: 'DESIGN_OPERATION_ACCEPTED',
        message: 'Notification dispatch was queued.',
        data: { id: 100, title: 'Thông báo', content: 'Nội dung', channels: ['PUSH'], status: 'QUEUED', created_at: '2026-11-21T10:00:00Z' },
        meta: { operation_id: operationId, notification_ids: [100] },
        traceId: 'trace-test',
      },
    }));
    await TestBed.configureTestingModule({
      imports: [AD20Page],
      providers: [
        provideRouter([]),
        { provide: AD20NotificationService, useValue: { getRecipients, createNotification } },
      ],
    }).compileComponents();
    const router = TestBed.inject(Router);
    vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);

    const fixture = TestBed.createComponent(AD20Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    expect(getRecipients).toHaveBeenCalledWith(1);
    expect(root.textContent).toContain('Student One');

    setInput(root, '#notice-title', 'Thông báo');
    setInput(root, '#notice-content', 'Nội dung');
    const recipient = root.querySelector<HTMLInputElement>('.recipient-results input')!;
    recipient.checked = true;
    recipient.dispatchEvent(new Event('change', { bubbles: true }));
    const channel = root.querySelector<HTMLInputElement>('.channel-options input[value="PUSH"]')!;
    channel.checked = true;
    channel.dispatchEvent(new Event('change', { bubbles: true }));
    fixture.detectChanges();

    root.querySelector<HTMLFormElement>('form')!.dispatchEvent(
      new Event('submit', { bubbles: true, cancelable: true }),
    );
    fixture.detectChanges();

    expect(createNotification).toHaveBeenCalledWith({
      recipients: [2001],
      title: 'Thông báo',
      content: 'Nội dung',
      channels: ['PUSH'],
    });
    expect(router.navigateByUrl).toHaveBeenCalledWith(
      `/operations/${operationId}`,
      { state: { sh07ReturnTo: '/admin/notifications/new' } },
    );
    expect(root.textContent).toContain('Chưa có xác nhận giao thông báo');
    expect(root.querySelector<HTMLButtonElement>('button[type="submit"]')?.disabled).toBe(true);
    setInput(root, '#notice-title', 'Thử gửi lần hai');
    fixture.detectChanges();
    expect(fixture.componentInstance.acceptedOperationId()).toBe(operationId);
    expect(fixture.componentInstance.title()).toBe('Thông báo');
    expect(createNotification).toHaveBeenCalledTimes(1);
  });

  it('locks the form after an accepted response without a valid operation UUID', async () => {
    const getRecipients = vi.fn((page: number) => of(recipientEnvelope(page)));
    const createNotification = vi.fn(() => of({
      status: 202,
      body: {
        success: true,
        businessCode: 'DESIGN_OPERATION_ACCEPTED',
        message: 'Notification dispatch was queued.',
        data: { id: 100, title: 'Thông báo', content: 'Nội dung', channels: ['PUSH'], status: 'QUEUED', created_at: '2026-11-21T10:00:00Z' },
        meta: {},
        traceId: 'trace-test',
      },
    }));
    await TestBed.configureTestingModule({
      imports: [AD20Page],
      providers: [
        provideRouter([]),
        { provide: AD20NotificationService, useValue: { getRecipients, createNotification } },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(AD20Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    setInput(root, '#notice-title', 'Thông báo');
    setInput(root, '#notice-content', 'Nội dung');
    const recipient = root.querySelector<HTMLInputElement>('.recipient-results input')!;
    recipient.checked = true;
    recipient.dispatchEvent(new Event('change', { bubbles: true }));
    const channel = root.querySelector<HTMLInputElement>('.channel-options input[value="PUSH"]')!;
    channel.checked = true;
    channel.dispatchEvent(new Event('change', { bubbles: true }));
    fixture.detectChanges();

    root.querySelector<HTMLFormElement>('form')!.dispatchEvent(
      new Event('submit', { bubbles: true, cancelable: true }),
    );
    fixture.detectChanges();

    expect(fixture.componentInstance.submissionUnconfirmed()).toBe(true);
    expect(root.querySelector('[role="alert"]')?.textContent).toContain('Không gửi lại');
    expect(root.querySelector('.return-link[href="/admin/notifications"]')?.textContent).toContain('Kiểm tra');
    expect(root.querySelector<HTMLInputElement>('#notice-title')?.disabled).toBe(true);
    expect(root.querySelector<HTMLButtonElement>('button[type="submit"]')?.disabled).toBe(true);

    fixture.componentInstance.submitNotification(new Event('submit') as SubmitEvent);
    expect(createNotification).toHaveBeenCalledTimes(1);
  });

  it('does not route a successful-looking #93 envelope unless HTTP status is 202', async () => {
    const getRecipients = vi.fn((page: number) => of(recipientEnvelope(page)));
    const createNotification = vi.fn(() => of({
      status: 200,
      body: {
        success: true,
        businessCode: 'DESIGN_OPERATION_ACCEPTED',
        message: 'Notification dispatch was queued.',
        data: { id: 100, title: 'Thông báo', content: 'Nội dung', channels: ['PUSH'], status: 'QUEUED', created_at: '2026-11-21T10:00:00Z' },
        meta: { operation_id: operationId, notification_ids: [100] },
        traceId: 'trace-test',
      },
    }));
    await TestBed.configureTestingModule({
      imports: [AD20Page],
      providers: [
        provideRouter([]),
        { provide: AD20NotificationService, useValue: { getRecipients, createNotification } },
      ],
    }).compileComponents();
    const router = TestBed.inject(Router);
    const navigate = vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);

    const fixture = TestBed.createComponent(AD20Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    setInput(root, '#notice-title', 'Thông báo');
    setInput(root, '#notice-content', 'Nội dung');
    const recipient = root.querySelector<HTMLInputElement>('.recipient-results input')!;
    recipient.checked = true;
    recipient.dispatchEvent(new Event('change', { bubbles: true }));
    const channel = root.querySelector<HTMLInputElement>('.channel-options input[value="PUSH"]')!;
    channel.checked = true;
    channel.dispatchEvent(new Event('change', { bubbles: true }));
    fixture.detectChanges();
    root.querySelector<HTMLFormElement>('form')!.dispatchEvent(
      new Event('submit', { bubbles: true, cancelable: true }),
    );
    fixture.detectChanges();

    expect(navigate).not.toHaveBeenCalled();
    expect(fixture.componentInstance.submissionUnconfirmed()).toBe(true);
    expect(root.querySelector('[role="alert"]')?.textContent).toContain('Không gửi lại');
  });

  it('reports API #93 403 as an access denial, not an invalid recipient', async () => {
    const getRecipients = vi.fn((page: number) => of(recipientEnvelope(page)));
    const createNotification = vi.fn(() => throwError(() => new HttpErrorResponse({
      status: 403,
      statusText: 'Forbidden',
    })));
    await TestBed.configureTestingModule({
      imports: [AD20Page],
      providers: [
        provideRouter([]),
        { provide: AD20NotificationService, useValue: { getRecipients, createNotification } },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(AD20Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    setInput(root, '#notice-title', 'Thông báo');
    setInput(root, '#notice-content', 'Nội dung');
    const recipient = root.querySelector<HTMLInputElement>('.recipient-results input')!;
    recipient.checked = true;
    recipient.dispatchEvent(new Event('change', { bubbles: true }));
    const channel = root.querySelector<HTMLInputElement>('.channel-options input[value="PUSH"]')!;
    channel.checked = true;
    channel.dispatchEvent(new Event('change', { bubbles: true }));
    fixture.detectChanges();

    root.querySelector<HTMLFormElement>('form')!.dispatchEvent(
      new Event('submit', { bubbles: true, cancelable: true }),
    );
    fixture.detectChanges();

    expect(root.querySelector('[role="alert"]')?.textContent).toContain('không có quyền tạo thông báo');
    expect(root.querySelector('[role="alert"]')?.textContent).not.toContain('người nhận');
    expect(fixture.componentInstance.submissionUnconfirmed()).toBe(false);
  });

  it('keeps a selected recipient when moving between API #68 pages', async () => {
    const getRecipients = vi.fn((page: number) => of(recipientEnvelope(page)));
    await TestBed.configureTestingModule({
      imports: [AD20Page],
      providers: [
        provideRouter([]),
        { provide: AD20NotificationService, useValue: { getRecipients, createNotification: vi.fn() } },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(AD20Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    const firstRecipient = root.querySelector<HTMLInputElement>('.recipient-results input')!;
    firstRecipient.checked = true;
    firstRecipient.dispatchEvent(new Event('change', { bubbles: true }));
    root.querySelectorAll<HTMLButtonElement>('.pagination-controls button')[1].click();
    fixture.detectChanges();

    expect(getRecipients).toHaveBeenCalledWith(1);
    expect(getRecipients).toHaveBeenCalledWith(2);
    expect(root.textContent).toContain('Student Two');
    expect(root.textContent).toContain('Đã chọn 1 người nhận');
    expect(root.querySelector('.selected-recipient-list')?.textContent).toContain('Student One');
  });
});

function setInput(root: HTMLElement, selector: string, value: string): void {
  const input = root.querySelector<HTMLInputElement | HTMLTextAreaElement>(selector);
  if (!input) throw new Error(`Missing ${selector}`);
  input.value = value;
  input.dispatchEvent(new Event('input', { bubbles: true }));
}

function recipientEnvelope(page: number) {
  const id = page === 1 ? 2001 : 2002;
  const fullName = page === 1 ? 'Student One' : 'Student Two';
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Users retrieved.',
    data: {
      items: [{
        id,
        full_name: fullName,
        email: `student-${id}@example.test`,
        role: 'STUDENT',
        avatar_url: null,
        phone: null,
        status: 'ACTIVE',
        created_at: '2026-11-20T10:00:00Z',
        updated_at: '2026-11-20T10:00:00Z',
      }],
      pagination: { page, size: 1, total: 2, total_pages: 2 },
    },
    meta: {},
    traceId: 'trace-test',
  };
}
