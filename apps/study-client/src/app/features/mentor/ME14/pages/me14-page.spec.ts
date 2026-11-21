import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { throwError } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { ME14NotificationCreateService } from '../data-access/me14-notification-create.service';
import { ME14Page } from './me14-page';

const operationId = 'a9a3c1b5-7ca4-4e77-9d0f-812b9506e18e';

describe('ME14Page notification handoff', () => {
  it('posts explicit handoff recipients as text and follows the accepted operation UUID', async () => {
    const create = vi.fn(() => of({
      success: true,
      businessCode: 'DESIGN_OPERATION_ACCEPTED',
      message: 'Notification dispatch was queued.',
      data: { id: operationId, kind: 'NOTIFICATION_DISPATCH', status: 'QUEUED' },
      meta: { notification_ids: [31, 32] },
      traceId: 'trace-test',
    }));
    await TestBed.configureTestingModule({
      imports: [ME14Page],
      providers: [
        provideRouter([]),
        { provide: ME14NotificationCreateService, useValue: { create } },
      ],
    }).compileComponents();
    const router = TestBed.inject(Router);
    vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);
    window.history.replaceState({
      courseId: 101,
      recipients: [
        { id: 2001, full_name: 'Student One' },
        { id: 2002, full_name: 'Student Two' },
      ],
    }, '', '/');

    const fixture = TestBed.createComponent(ME14Page);
    fixture.detectChanges();
    const component = fixture.componentInstance;
    expect(history.state.recipients).toBeUndefined();
    component.title.set('Thông báo lịch học');
    component.content.set('Buổi học bắt đầu lúc 09:00.');
    component.channels.set(['PUSH', 'EMAIL']);
    fixture.detectChanges();

    const form = fixture.nativeElement.querySelector('form') as HTMLFormElement;
    form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    fixture.detectChanges();

    expect(create).toHaveBeenCalledWith(
      '2001,2002',
      'Thông báo lịch học',
      'Buổi học bắt đầu lúc 09:00.',
      'PUSH,EMAIL',
    );
    expect(router.navigateByUrl).toHaveBeenCalledWith(
      `/operations/${operationId}`,
      { state: { sh07ReturnTo: '/mentor/notifications/new' } },
    );
    component.updateTitle('Sửa sau khi đã xếp hàng');
    expect(component.title()).toBe('Thông báo lịch học');
    expect(component.canSubmit()).toBe(false);
    expect(create).toHaveBeenCalledOnce();
  });

  it('blocks a blind resend after a network failure leaves the #63 outcome uncertain', async () => {
    const create = vi.fn(() => throwError(() => new HttpErrorResponse({ status: 0 })));
    await TestBed.configureTestingModule({
      imports: [ME14Page],
      providers: [
        provideRouter([]),
        { provide: ME14NotificationCreateService, useValue: { create } },
      ],
    }).compileComponents();
    window.history.replaceState({
      courseId: 101,
      recipients: [{ id: 2001, full_name: 'Student One' }],
    }, '', '/');

    const fixture = TestBed.createComponent(ME14Page);
    fixture.detectChanges();
    const component = fixture.componentInstance;
    component.title.set('Thông báo lịch học');
    component.content.set('Buổi học bắt đầu lúc 09:00.');
    component.channels.set(['PUSH']);
    fixture.detectChanges();

    const form = fixture.nativeElement.querySelector('form') as HTMLFormElement;
    form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    fixture.detectChanges();

    expect(component.submissionUncertain()).toBe(true);
    expect(component.canSubmit()).toBe(false);
    expect(fixture.nativeElement.textContent).toContain('không có khóa chống trùng');
    form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    fixture.detectChanges();
    expect(create).toHaveBeenCalledOnce();
  });
});
