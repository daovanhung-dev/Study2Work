import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { ST20ProgressService } from './st20-progress.service';

describe('ST20ProgressService', () => {
  let request: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    request = vi.fn().mockReturnValue(of({ success: true, data: {} }));

    await TestBed.configureTestingModule({
      providers: [
        ST20ProgressService,
        { provide: StudentApiService, useValue: { request } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('calls API #38 without a client-supplied user identity', () => {
    TestBed.inject(ST20ProgressService).achievements().subscribe();

    expect(request).toHaveBeenCalledTimes(1);
    expect(request.mock.calls[0]).toEqual([STUDY_SERVER_APIS.API_038]);
  });
});
