import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { ST25ThreadService } from './st25-thread.service';

describe('ST25ThreadService', () => {
  let request: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    request = vi.fn().mockReturnValue(of({ success: true, data: {} }));

    await TestBed.configureTestingModule({
      providers: [
        ST25ThreadService,
        { provide: StudentApiService, useValue: { request } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('maps the discussion ID to API #42 thread lookup', () => {
    TestBed.inject(ST25ThreadService).thread('91').subscribe();

    expect(request).toHaveBeenCalledTimes(1);
    expect(request.mock.calls[0]).toEqual([
      STUDY_SERVER_APIS.API_042,
      { pathParams: { discussion_id: '91' } },
    ]);
  });

  it('sends only the current server-backed content field to API #41', () => {
    TestBed.inject(ST25ThreadService).reply('91', 'A reply').subscribe();

    expect(request).toHaveBeenCalledTimes(1);
    expect(request.mock.calls[0]).toEqual([
      STUDY_SERVER_APIS.API_041,
      { pathParams: { discussion_id: '91' }, body: { content: 'A reply' } },
    ]);
  });
});
