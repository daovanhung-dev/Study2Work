import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { ST16ResultService } from './st16-result.service';

describe('ST16ResultService', () => {
  let request: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    request = vi.fn().mockReturnValue(of({ success: true, data: {} }));

    await TestBed.configureTestingModule({
      providers: [
        ST16ResultService,
        { provide: StudentApiService, useValue: { request } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('maps the route attempt ID to API #32 without adding other request fields', () => {
    TestBed.inject(ST16ResultService).result('42').subscribe();

    expect(request).toHaveBeenCalledTimes(1);
    expect(request).toHaveBeenCalledWith(STUDY_SERVER_APIS.API_032, {
      pathParams: { attempt_id: '42' },
    });
  });
});
