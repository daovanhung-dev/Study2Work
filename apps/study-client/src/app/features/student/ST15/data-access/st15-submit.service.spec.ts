import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { ST15SubmitService } from './st15-submit.service';

describe('ST15SubmitService', () => {
  let apiRequest: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    apiRequest = vi.fn().mockReturnValue(of({}));
    TestBed.configureTestingModule({
      providers: [
        ST15SubmitService,
        { provide: StudentApiService, useValue: { request: apiRequest } },
      ],
    });
  });

  afterEach(() => TestBed.resetTestingModule());

  it('sends the attempt ID to API #31 as the path parameter', () => {
    TestBed.inject(ST15SubmitService).submit('42').subscribe();

    expect(apiRequest).toHaveBeenCalledTimes(1);
    expect(apiRequest).toHaveBeenCalledWith(STUDY_SERVER_APIS.API_031, {
      pathParams: { attempt_id: '42' },
    });
  });
});
