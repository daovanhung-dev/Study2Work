import { HttpParams } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import { ME01DashboardService } from './me01-dashboard.service';

describe('ME01DashboardService', () => {
  it('uses the supported page query for #54 and keeps the four-course preview on #46', () => {
    const request = vi.fn((_api: unknown, _options?: { params?: HttpParams }) => of({}));
    TestBed.configureTestingModule({
      providers: [
        ME01DashboardService,
        { provide: MentorApiService, useValue: { request } },
      ],
    });

    const service = TestBed.inject(ME01DashboardService);
    service.courses();
    service.submissions();
    service.support();

    expect(request).toHaveBeenNthCalledWith(1, STUDY_SERVER_APIS.API_046, {
      params: expect.any(HttpParams),
    });
    expect(request.mock.calls[0]?.[1]?.params?.toString()).toBe('page=1&size=4');
    expect(request).toHaveBeenNthCalledWith(2, STUDY_SERVER_APIS.API_054, {
      params: expect.any(HttpParams),
    });
    expect(request.mock.calls[1]?.[1]?.params?.toString()).toBe('page=1');
    expect(request).toHaveBeenNthCalledWith(3, STUDY_SERVER_APIS.API_058);
  });
});
