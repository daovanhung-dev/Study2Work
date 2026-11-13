import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';
import { Me15NotificationStatusService } from '../data-access/me15-notification-status.service';
import { ME15Page } from './me15-page';

describe('ME15Page', () => {
  function setup(params: Record<string, string> = {}, queryParams: Record<string, string> = {}) {
    const serviceMock: Pick<Me15NotificationStatusService, 'getBatchStatuses'> = {
      getBatchStatuses: vi.fn().mockReturnValue(
        of([
          { notificationId: 900, operationId: 'notif-op-900', status: 'SENT' },
          { notificationId: 901, operationId: 'notif-op-901', status: 'QUEUED' },
        ]),
      ),
    };

    TestBed.configureTestingModule({
      imports: [ME15Page],
      providers: [
        provideRouter([]),
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: convertToParamMap(params),
              queryParamMap: convertToParamMap(queryParams),
            },
          },
        },
        { provide: Me15NotificationStatusService, useValue: serviceMock },
      ],
    });

    const fixture: ComponentFixture<ME15Page> = TestBed.createComponent(ME15Page);
    return { fixture, component: fixture.componentInstance, service: serviceMock };
  }

  it('loads notification statuses (#64) from queryParams ids and computes summary counts', () => {
    const { fixture, component, service } = setup({}, { ids: '900,901' });
    fixture.detectChanges();

    expect(service.getBatchStatuses).toHaveBeenCalledWith([900, 901]);
    expect(component.summary().total).toBe(2);
    expect(component.summary().sent).toBe(1);
    expect(component.summary().queued).toBe(1);
    expect(component.summary().failed).toBe(0);

    const rows = (fixture.nativeElement as HTMLElement).querySelectorAll('[data-testid="status-row"]');
    expect(rows.length).toBe(2);
  });

  it('supports single notificationId path param (/mentor/notifications/:notificationId/status)', () => {
    const { fixture, service } = setup({ notificationId: '900' }, {});
    fixture.detectChanges();

    expect(service.getBatchStatuses).toHaveBeenCalledWith([900]);
  });

  it('shows INVALID_NOTIFICATION_ID error when route notificationId is non-numeric', () => {
    const { fixture, component, service } = setup({ notificationId: 'bad-id' }, {});
    fixture.detectChanges();

    expect(service.getBatchStatuses).not.toHaveBeenCalled();
    expect(component.errorCode()).toBe('INVALID_NOTIFICATION_ID');
  });
});
