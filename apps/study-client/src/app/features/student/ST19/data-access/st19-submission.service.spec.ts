import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { ST19SubmissionService } from './st19-submission.service';

describe('ST19SubmissionService', () => {
  let request: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    request = vi.fn().mockReturnValue(of({ success: true, data: {} }));

    await TestBed.configureTestingModule({
      providers: [
        ST19SubmissionService,
        { provide: StudentApiService, useValue: { request } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('maps the route submission ID to API #36 without adding other request fields', () => {
    TestBed.inject(ST19SubmissionService).submission('54').subscribe();

    expect(request).toHaveBeenCalledTimes(1);
    expect(request).toHaveBeenCalledWith(STUDY_SERVER_APIS.API_036, {
      pathParams: { submission_id: '54' },
    });
  });
});
