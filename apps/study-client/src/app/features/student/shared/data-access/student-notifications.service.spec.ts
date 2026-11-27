import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { ST26NotificationsService } from '../../ST26/data-access/st26-notifications.service';

describe('ST26NotificationsService', () => {
  let request: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    request = vi.fn().mockReturnValue(of({ success: true, data: {} }));

    await TestBed.configureTestingModule({
      providers: [
        ST26NotificationsService,
        { provide: StudentApiService, useValue: { request } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('maps list filters to API #43 query parameters', () => {
    TestBed.inject(ST26NotificationsService).list(true, 3).subscribe();

    expect(request).toHaveBeenCalledTimes(1);
    const [api, options] = request.mock.calls[0];
    expect(api).toBe(STUDY_SERVER_APIS.API_043);
    expect(options.params.keys()).toEqual(['unread_only', 'page']);
    expect(options.params.get('unread_only')).toBe('true');
    expect(options.params.get('page')).toBe('3');
    expect(options.pathParams).toBeUndefined();
    expect(options.body).toBeUndefined();
  });

  it('maps a single read action to API #44 path parameters', () => {
    TestBed.inject(ST26NotificationsService).markRead('731').subscribe();

    expect(request.mock.calls).toEqual([
      [STUDY_SERVER_APIS.API_044, { pathParams: { notification_id: '731' } }],
    ]);
  });

  it('calls API #45 without adding uncontracted request fields', () => {
    TestBed.inject(ST26NotificationsService).markAllRead().subscribe();

    expect(request.mock.calls).toEqual([[STUDY_SERVER_APIS.API_045]]);
  });
});
