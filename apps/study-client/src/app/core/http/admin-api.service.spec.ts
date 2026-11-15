import { HttpErrorResponse, HttpParams, provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { AdminSessionService } from '../auth/admin-session.service';
import { STUDY_SERVER_APIS } from '../constant/api.constants';
import type { ApiEnvelope } from './api-envelope';
import { AdminApiService } from './admin-api.service';

interface TestAuthPayload {
  full_name: string;
  email: string;
  role: string;
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  refresh_expires_in: number;
}

describe('AdminSessionService and AdminApiService', () => {
  let session: AdminSessionService;
  let adminApi: AdminApiService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    session = TestBed.inject(AdminSessionService);
    adminApi = TestBed.inject(AdminApiService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    http.verify();
    vi.useRealTimers();
  });

  it('sends the exact login body and accepts an Admin source profile in memory', async () => {
    const login = firstValueFrom(session.login('admin@example.test', '  exact password  '));
    const request = http.expectOne('/api/v1/auth/login');

    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual({
      email: 'admin@example.test',
      password: '  exact password  ',
    });
    expect(request.request.headers.has('Authorization')).toBe(false);

    request.flush(successEnvelope(adminPayload()));
    await expect(login).resolves.toBeUndefined();
    expect(session.profile()).toEqual({
      full_name: 'Admin User',
      email: 'admin@example.test',
      role: 'ADMIN',
    });
    expect(session.isAuthenticated()).toBe(true);
  });

  it('rejects a valid login whose returned role is not Admin without keeping its token', async () => {
    const login = firstValueFrom(session.login('student@example.test', 'password'));
    http.expectOne('/api/v1/auth/login').flush(successEnvelope(adminPayload({ role: 'STUDENT' })));

    await expect(login).rejects.toMatchObject({
      code: 'ADMIN_ROLE_REQUIRED',
    });
    expect(session.profile()).toBeNull();
    expect(session.isAuthenticated()).toBe(false);
    http.expectNone('/api/v1/auth/refresh');
  });

  it('rotates refresh credentials only after the locally tracked access token expires', async () => {
    vi.useFakeTimers();
    const login = firstValueFrom(session.login('admin@example.test', 'password'));
    http.expectOne('/api/v1/auth/login').flush(successEnvelope(adminPayload({ expires_in: 1 })));
    await login;
    vi.advanceTimersByTime(1000);

    const token = firstValueFrom(session.getAdminAccessToken());
    const refresh = http.expectOne('/api/v1/auth/refresh');
    expect(refresh.request.method).toBe('POST');
    expect(refresh.request.body).toEqual({ refresh_token: 'refresh-token-1' });
    refresh.flush(successEnvelope(adminPayload({
      access_token: 'access-token-2',
      refresh_token: 'refresh-token-2',
      expires_in: 60,
    })));

    await expect(token).resolves.toBe('access-token-2');
    expect(session.isAuthenticated()).toBe(true);
  });

  it('adds Bearer authorization and forwards exact filters for a protected read', async () => {
    await signIn(session, http);
    const response = firstValueFrom(
      adminApi.get<{ items: unknown[] }>(STUDY_SERVER_APIS.API_068, {
        params: new HttpParams()
          .set('keyword', 'mai@example.test')
          .set('role', 'MENTOR')
          .set('page', '2'),
      }),
    );

    const request = http.expectOne((candidate) =>
      candidate.url === '/api/v1/admin/users'
      && candidate.params.get('keyword') === 'mai@example.test'
      && candidate.params.get('role') === 'MENTOR'
      && candidate.params.get('page') === '2',
    );
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(successEnvelope({ items: [] }));
    await expect(response).resolves.toMatchObject({ data: { items: [] } });
  });

  it('does not issue unauthenticated reads and clears the local session on a protected 401', async () => {
    const withoutSession = firstValueFrom(adminApi.get(STUDY_SERVER_APIS.API_068));
    await expect(withoutSession).rejects.toMatchObject({ code: 'LOGIN_REQUIRED' });
    http.expectNone('/api/v1/admin/users');

    await signIn(session, http);
    const rejectedRead = firstValueFrom(adminApi.get(STUDY_SERVER_APIS.API_068));
    http.expectOne('/api/v1/admin/users').flush({}, { status: 401, statusText: 'Unauthorized' });
    await expect(rejectedRead).rejects.toBeInstanceOf(HttpErrorResponse);
    expect(session.isAuthenticated()).toBe(false);
  });

  it('rejects writes through the Admin read-only API client before sending HTTP', () => {
    expect(() => adminApi.get(STUDY_SERVER_APIS.API_071)).toThrow(/WIRED GET/);
    http.expectNone((request) => request.url.startsWith('/api/v1'));
  });
});

function adminPayload(overrides: Partial<TestAuthPayload> = {}): TestAuthPayload {
  return {
    full_name: 'Admin User',
    email: 'admin@example.test',
    role: 'ADMIN',
    access_token: 'access-token-1',
    refresh_token: 'refresh-token-1',
    token_type: 'bearer',
    expires_in: 60,
    refresh_expires_in: 3600,
    ...overrides,
  };
}

function successEnvelope<T>(data: T): ApiEnvelope<T> {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'ok',
    data,
    meta: {},
    traceId: 'test-trace',
  };
}

async function signIn(session: AdminSessionService, http: HttpTestingController): Promise<void> {
  const login = firstValueFrom(session.login('admin@example.test', 'password'));
  http.expectOne('/api/v1/auth/login').flush(successEnvelope(adminPayload()));
  await login;
}
