import { HttpErrorResponse, provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { StudentSessionService } from '../auth/student-session.service';
import { STUDY_SERVER_APIS } from '../constant/api.constants';
import type { ApiEnvelope } from './api-envelope';
import { StudentApiService } from './student-api.service';

describe('StudentApiService API #04 refresh/replay', () => {
  let session: StudentSessionService;
  let api: StudentApiService;
  let http: HttpTestingController;
  let router: Router;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    });
    session = TestBed.inject(StudentSessionService);
    api = TestBed.inject(StudentApiService);
    http = TestBed.inject(HttpTestingController);
    router = TestBed.inject(Router);
    vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);
  });

  afterEach(() => http.verify());

  it('refreshes once after an API #04 401 and retries the profile read with the new token', async () => {
    await signIn(session, http);
    const profile = firstValueFrom(api.request(STUDY_SERVER_APIS.API_004));

    http.expectOne('/api/v1/users/me').flush(authError(401), {
      status: 401,
      statusText: 'Unauthorized',
    });
    const refresh = http.expectOne('/api/v1/auth/refresh');
    expect(refresh.request.method).toBe('POST');
    expect(refresh.request.body).toEqual({ refresh_token: 'refresh-token-1' });
    refresh.flush(successEnvelope(studentPayload({
      access_token: 'access-token-2',
      refresh_token: 'refresh-token-2',
    })));

    const retriedProfile = http.expectOne('/api/v1/users/me');
    expect(retriedProfile.request.headers.get('Authorization')).toBe('Bearer access-token-2');
    retriedProfile.flush(successEnvelope({ email: 'student@example.test', role: 'STUDENT' }));

    await expect(profile).resolves.toMatchObject({ success: true });
    expect(session.isAuthenticated()).toBe(true);
    http.expectNone('/api/v1/auth/refresh');
  });

  it('does not refresh after API #04 returns 403 and sends a safe SH-05 route handoff', async () => {
    await signIn(session, http);
    const profile = firstValueFrom(api.request(STUDY_SERVER_APIS.API_004));
    http.expectOne('/api/v1/users/me').flush(authError(403), {
      status: 403,
      statusText: 'Forbidden',
    });

    await expect(profile).rejects.toBeInstanceOf(HttpErrorResponse);
    http.expectNone('/api/v1/auth/refresh');
    expect(session.isAuthenticated()).toBe(true);
    expect(router.navigateByUrl).toHaveBeenCalledWith('/forbidden', {
      state: expect.objectContaining({ sh05ReturnTo: '/' }),
    });
  });

  it('ends the session after the single profile retry also returns 401', async () => {
    await signIn(session, http);
    const profile = firstValueFrom(api.request(STUDY_SERVER_APIS.API_004));
    http.expectOne('/api/v1/users/me').flush(authError(401), {
      status: 401,
      statusText: 'Unauthorized',
    });
    http.expectOne('/api/v1/auth/refresh').flush(successEnvelope(studentPayload({
      access_token: 'access-token-2',
      refresh_token: 'refresh-token-2',
    })));
    http.expectOne('/api/v1/users/me').flush(authError(401), {
      status: 401,
      statusText: 'Unauthorized',
    });

    await expect(profile).rejects.toBeInstanceOf(HttpErrorResponse);
    expect(session.isAuthenticated()).toBe(false);
    http.expectNone('/api/v1/auth/refresh');
  });
});

async function signIn(session: StudentSessionService, http: HttpTestingController): Promise<void> {
  const login = firstValueFrom(session.login('student@example.test', 'password'));
  http.expectOne('/api/v1/auth/login').flush(successEnvelope(studentPayload()));
  await login;
}

function studentPayload(overrides: Record<string, unknown> = {}) {
  return {
    full_name: 'Student User',
    email: 'student@example.test',
    role: 'STUDENT',
    access_token: 'access-token-1',
    refresh_token: 'refresh-token-1',
    token_type: 'bearer',
    expires_in: 3600,
    refresh_expires_in: 7200,
    ...overrides,
  };
}

function successEnvelope<T>(data: T): ApiEnvelope<T> {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Resource retrieved.',
    data,
    meta: {},
    traceId: 'test-trace',
  };
}

function authError(status: 401 | 403): Record<string, unknown> {
  return {
    success: false,
    businessCode: status === 401
      ? 'DESIGN_AUTHENTICATION_REQUIRED'
      : 'DESIGN_ACCESS_DENIED',
    message: status === 401 ? 'Authentication required.' : 'Access denied.',
    data: null,
    meta: {},
    traceId: `trace-${status}`,
  };
}
