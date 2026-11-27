import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import { ME12SupportThreadService } from './me12-support-thread.service';

describe('ME12SupportThreadService', () => {
  let request: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    request = vi.fn().mockReturnValue(of({ success: true, data: {} }));

    await TestBed.configureTestingModule({
      providers: [
        ME12SupportThreadService,
        { provide: MentorApiService, useValue: { request } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('maps the route request ID to API #59', () => {
    TestBed.inject(ME12SupportThreadService).detail('41').subscribe();

    expect(request).toHaveBeenCalledExactlyOnceWith(STUDY_SERVER_APIS.API_059, {
      pathParams: { request_id: '41' },
    });
  });

  it('maps an explicit reply to API #60 with the current empty attachment reference', () => {
    TestBed.inject(ME12SupportThreadService).reply('41', 'Please review this issue.').subscribe();

    expect(request).toHaveBeenCalledExactlyOnceWith(STUDY_SERVER_APIS.API_060, {
      pathParams: { request_id: '41' },
      body: { message: 'Please review this issue.', attachment_refs: '[]' },
    });
  });
});
