import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { ST12ResourcesService } from './st12-resources.service';

describe('ST12ResourcesService', () => {
  let request: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    request = vi.fn().mockReturnValue(of({ success: true, data: {} }));

    await TestBed.configureTestingModule({
      providers: [
        ST12ResourcesService,
        { provide: StudentApiService, useValue: { request } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('maps the route lesson ID to API #26 without extra request fields', () => {
    TestBed.inject(ST12ResourcesService).resources('42').subscribe();

    expect(request).toHaveBeenCalledExactlyOnceWith(STUDY_SERVER_APIS.API_026, {
      pathParams: { lesson_id: '42' },
    });
  });
});
