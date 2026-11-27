import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { ST21CourseProgressService } from './st21-course-progress.service';

describe('ST21CourseProgressService', () => {
  let request: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    request = vi.fn().mockReturnValue(of({ success: true, data: {} }));

    await TestBed.configureTestingModule({
      providers: [
        ST21CourseProgressService,
        { provide: StudentApiService, useValue: { request } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('maps the route course ID to API #37 without a client-supplied user identity', () => {
    TestBed.inject(ST21CourseProgressService).progress('42').subscribe();

    expect(request.mock.calls).toEqual([
      [STUDY_SERVER_APIS.API_037, { pathParams: { course_id: '42' } }],
    ]);
  });
});
