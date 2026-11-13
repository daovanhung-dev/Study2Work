import { HttpHeaders, HttpParams, provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { STUDY_SERVER_APIS } from '../constant/api.constants';
import type { ApiEnvelope } from './api-envelope';
import { StudyApiService } from './study-api.service';

describe('Study Server API registry', () => {
  it('contains all catalog IDs and distinguishes source status', () => {
    const entries = Object.values(STUDY_SERVER_APIS);
    const catalogIds = entries.flatMap((api) => (typeof api.id === 'number' ? [api.id] : []));

    expect(entries).toHaveLength(104);
    expect(catalogIds.sort((first, second) => first - second)).toEqual(
      Array.from({ length: 103 }, (_value, index) => index + 1),
    );
    expect(entries.filter((api) => api.status === 'WIRED')).toHaveLength(65);
    expect(entries.filter((api) => api.status === 'STUB')).toHaveLength(1);
    expect(entries.filter((api) => api.status === 'UNWIRED')).toHaveLength(37);
    expect(entries.filter((api) => api.status === 'SOURCE_ONLY')).toHaveLength(1);

    expect(STUDY_SERVER_APIS.API_002).toMatchObject({
      id: 2,
      method: 'POST',
      path: '/auth/verify-email/send',
      status: 'STUB',
    });
    expect(STUDY_SERVER_APIS.API_003_REFRESH).toMatchObject({
      id: 'R-X01',
      relatedApiId: 3,
      method: 'POST',
      path: '/auth/refresh',
      status: 'SOURCE_ONLY',
    });
  });
});

describe('StudyApiService', () => {
  let api: StudyApiService;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });

    api = TestBed.inject(StudyApiService);
    httpTestingController = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTestingController.verify();
  });

  it('uses the descriptor method and forwards body and headers', async () => {
    const body = { full_name: 'Mai Nguyen', bio: '', phone: '' };
    const headers = new HttpHeaders({
      Authorization: 'Bearer test-token',
      'X-Trace-Id': 'client-trace',
    });
    const expected: ApiEnvelope<{ updated: boolean }> = {
      success: true,
      businessCode: 'DESIGN_RESOURCE_UPDATED',
      message: 'Profile updated',
      data: { updated: true },
      meta: {},
      traceId: 'server-trace',
    };
    const response = firstValueFrom(
      api.request<{ updated: boolean }>(STUDY_SERVER_APIS.API_014, { body, headers }),
    );

    const request = httpTestingController.expectOne('/api/v1/users/me/profile');
    expect(request.request.method).toBe('PUT');
    expect(request.request.body).toEqual(body);
    expect(request.request.headers.get('Authorization')).toBe('Bearer test-token');
    expect(request.request.headers.get('X-Trace-Id')).toBe('client-trace');

    request.flush(expected);
    await expect(response).resolves.toEqual(expected);
  });

  it('forwards query parameters', async () => {
    const params = new HttpParams().set('locale', 'vi');
    const expected: ApiEnvelope<string[]> = {
      success: true,
      businessCode: 'DESIGN_RESOURCE_RETRIEVED',
      message: 'Categories loaded',
      data: ['Toán'],
      meta: {},
      traceId: 'server-trace',
    };
    const response = firstValueFrom(api.request<string[]>(STUDY_SERVER_APIS.API_005, { params }));

    const request = httpTestingController.expectOne((candidate) => {
      return candidate.url === '/api/v1/categories' && candidate.params.get('locale') === 'vi';
    });
    expect(request.request.method).toBe('GET');

    request.flush(expected);
    await expect(response).resolves.toEqual(expected);
  });

  it('URL-encodes dynamic path parameters', async () => {
    const expected: ApiEnvelope<{ id: string }> = {
      success: true,
      businessCode: 'DESIGN_RESOURCE_RETRIEVED',
      message: 'Course loaded',
      data: { id: 'course/intro 1' },
      meta: {},
      traceId: 'server-trace',
    };
    const response = firstValueFrom(
      api.request<{ id: string }>(STUDY_SERVER_APIS.API_008, {
        pathParams: { course_id: 'course/intro 1' },
      }),
    );

    const request = httpTestingController.expectOne('/api/v1/courses/course%2Fintro%201');
    expect(request.request.method).toBe('GET');

    request.flush(expected);
    await expect(response).resolves.toEqual(expected);
  });

  it('rejects missing path parameters before sending HTTP', () => {
    expect(() => api.request(STUDY_SERVER_APIS.API_008)).toThrow(/course_id/);
    httpTestingController.expectNone((request) => request.url.startsWith('/api/v1'));
  });

  it('rejects unwired APIs before sending HTTP', () => {
    expect(() => api.request(STUDY_SERVER_APIS.API_010)).toThrow(/UNWIRED/);
    httpTestingController.expectNone((request) => request.url.startsWith('/api/v1'));
  });

  it('allows the source-only refresh route through the descriptor', async () => {
    const body = { refresh_token: 'opaque-test-token' };
    const expected: ApiEnvelope<{ access_token: string }> = {
      success: true,
      businessCode: 'DESIGN_RESOURCE_UPDATED',
      message: 'Token refreshed',
      data: { access_token: 'new-access-token' },
      meta: {},
      traceId: 'server-trace',
    };
    const response = firstValueFrom(
      api.request<{ access_token: string }>(STUDY_SERVER_APIS.API_003_REFRESH, { body }),
    );

    const request = httpTestingController.expectOne('/api/v1/auth/refresh');
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual(body);

    request.flush(expected);
    await expect(response).resolves.toEqual(expected);
  });
});
