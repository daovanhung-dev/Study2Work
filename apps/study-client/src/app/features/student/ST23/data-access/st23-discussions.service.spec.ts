import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { ST23DiscussionsService } from './st23-discussions.service';

describe('ST23DiscussionsService', () => {
  let request: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    request = vi.fn().mockReturnValue(of({ success: true, data: {} }));

    await TestBed.configureTestingModule({
      providers: [
        ST23DiscussionsService,
        { provide: StudentApiService, useValue: { request } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('maps the requested page and course filter to API #39', () => {
    TestBed.inject(ST23DiscussionsService).discussions(42, 3).subscribe();

    expect(request).toHaveBeenCalledTimes(1);
    const [api, options] = request.mock.calls[0];
    expect(api).toBe(STUDY_SERVER_APIS.API_039);
    expect(options.params.keys()).toEqual(['page', 'course_id']);
    expect(options.params.get('page')).toBe('3');
    expect(options.params.get('course_id')).toBe('42');
    expect(options.pathParams).toBeUndefined();
    expect(options.body).toBeUndefined();
  });

  it('omits the optional course filter when none is selected', () => {
    TestBed.inject(ST23DiscussionsService).discussions(null, 1).subscribe();

    expect(request).toHaveBeenCalledTimes(1);
    const [api, options] = request.mock.calls[0];
    expect(api).toBe(STUDY_SERVER_APIS.API_039);
    expect(options.params.keys()).toEqual(['page']);
    expect(options.params.get('page')).toBe('1');
    expect(options.params.get('course_id')).toBeNull();
  });
});
