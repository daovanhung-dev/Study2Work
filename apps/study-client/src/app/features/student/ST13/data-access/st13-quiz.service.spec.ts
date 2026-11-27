import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { ST13QuizService } from './st13-quiz.service';

describe('ST13QuizService', () => {
  let request: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    request = vi.fn().mockReturnValue(of({ success: true, data: {} }));

    await TestBed.configureTestingModule({
      providers: [
        ST13QuizService,
        { provide: StudentApiService, useValue: { request } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('maps the route quiz ID to API #28', () => {
    TestBed.inject(ST13QuizService).quiz('28').subscribe();

    expect(request).toHaveBeenCalledExactlyOnceWith(STUDY_SERVER_APIS.API_028, {
      pathParams: { quiz_id: '28' },
    });
  });

  it('maps explicit attempt creation to API #29 without an invented body', () => {
    TestBed.inject(ST13QuizService).start('28').subscribe();

    expect(request).toHaveBeenCalledExactlyOnceWith(STUDY_SERVER_APIS.API_029, {
      pathParams: { quiz_id: '28' },
    });
  });
});
