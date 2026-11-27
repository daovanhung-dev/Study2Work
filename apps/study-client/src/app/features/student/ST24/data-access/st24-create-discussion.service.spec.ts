import { HttpParams } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { ST24CreateDiscussionService } from './st24-create-discussion.service';

describe('ST24CreateDiscussionService', () => {
  let request: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    request = vi.fn().mockReturnValue(of({ success: true, data: {} }));

    await TestBed.configureTestingModule({
      providers: [
        ST24CreateDiscussionService,
        { provide: StudentApiService, useValue: { request } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('requests active enrolled courses from API #20 with the requested page', () => {
    TestBed.inject(ST24CreateDiscussionService).courses(3).subscribe();

    expect(request).toHaveBeenCalledTimes(1);
    const [api, options] = request.mock.calls[0] as [
      string,
      { params?: HttpParams; body?: unknown },
    ];
    expect(api).toBe(STUDY_SERVER_APIS.API_020);
    expect(options.params?.get('status')).toBe('ACTIVE');
    expect(options.params?.get('page')).toBe('3');
    expect(options.body).toBeUndefined();
  });

  it('sends the current server-backed string content payload to API #40', () => {
    TestBed.inject(ST24CreateDiscussionService)
      .create(17, 'Question title', 'Question body')
      .subscribe();

    expect(request).toHaveBeenCalledTimes(1);
    expect(request).toHaveBeenCalledWith(STUDY_SERVER_APIS.API_040, {
      body: { course_id: 17, title: 'Question title', content: 'Question body' },
    });
  });

  it('refreshes API #39 for the requested course on page one', () => {
    TestBed.inject(ST24CreateDiscussionService).refresh(17).subscribe();

    expect(request).toHaveBeenCalledTimes(1);
    const [api, options] = request.mock.calls[0] as [
      string,
      { params?: HttpParams; body?: unknown },
    ];
    expect(api).toBe(STUDY_SERVER_APIS.API_039);
    expect(options.params?.get('course_id')).toBe('17');
    expect(options.params?.get('page')).toBe('1');
    expect(options.body).toBeUndefined();
  });
});
