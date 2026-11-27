import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { ST14AttemptService } from './st14-attempt.service';

describe('ST14AttemptService', () => {
  let request: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    request = vi.fn().mockReturnValue(of({ success: true, data: {} }));

    await TestBed.configureTestingModule({
      providers: [
        ST14AttemptService,
        { provide: StudentApiService, useValue: { request } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('maps the route quiz ID to API #28', () => {
    TestBed.inject(ST14AttemptService).quiz('28').subscribe();

    expect(request).toHaveBeenCalledExactlyOnceWith(STUDY_SERVER_APIS.API_028, {
      pathParams: { quiz_id: '28' },
    });
  });

  it('maps the route attempt and current answer payload to API #30', () => {
    TestBed.inject(ST14AttemptService).save('501', 31, [101, 102]).subscribe();

    expect(request).toHaveBeenCalledExactlyOnceWith(STUDY_SERVER_APIS.API_030, {
      pathParams: { attempt_id: '501' },
      body: { question_id: 31, choice_ids: [101, 102] },
    });
  });
});
