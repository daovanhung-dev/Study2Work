import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { MentorSessionService } from '../auth/mentor-session.service';
import { STUDY_SERVER_APIS } from '../constant/api.constants';
import type { ApiEnvelope } from './api-envelope';
import { MentorApiService } from './mentor-api.service';

describe('MentorApiService', () => {
  let session: MentorSessionService;
  let api: MentorApiService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    session = TestBed.inject(MentorSessionService);
    api = TestBed.inject(MentorApiService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('allows the source-backed shared API #18 operation read for a Mentor session', async () => {
    const login = firstValueFrom(session.login('mentor@example.test', 'password'));
    http.expectOne('/api/v1/auth/login').flush(successEnvelope(mentorPayload()));
    await login;

    const operationId = 'b46e19e7-4ef2-4a4f-9ed2-83783e68fb01';
    const response = firstValueFrom(api.request(STUDY_SERVER_APIS.API_018, {
      pathParams: { operation_id: operationId },
    }));
    const request = http.expectOne(`/api/v1/operations/${operationId}`);
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer mentor-token');
    request.flush(successEnvelope({
      id: operationId,
      kind: 'NOTIFICATION_DISPATCH',
      status: 'QUEUED',
      owner_id: 1001,
      submitted_at: '2026-11-20T10:00:00Z',
      updated_at: '2026-11-20T10:00:00Z',
    }, 'DESIGN_OPERATION_RETRIEVED'));
    await expect(response).resolves.toMatchObject({ businessCode: 'DESIGN_OPERATION_RETRIEVED' });
  });
});

function mentorPayload() {
  return {
    full_name: 'Mentor User',
    email: 'mentor@example.test',
    role: 'MENTOR',
    access_token: 'mentor-token',
    refresh_token: 'mentor-refresh-token',
    token_type: 'bearer',
    expires_in: 3600,
    refresh_expires_in: 7200,
  };
}

function successEnvelope<T>(data: T, businessCode = 'DESIGN_RESOURCE_RETRIEVED'): ApiEnvelope<T> {
  return {
    success: true,
    businessCode,
    message: 'Resource retrieved.',
    data,
    meta: {},
    traceId: 'trace-test',
  };
}
