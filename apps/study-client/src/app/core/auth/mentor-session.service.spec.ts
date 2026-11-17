import { firstValueFrom } from 'rxjs';

import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { MentorSessionService } from './mentor-session.service';
import { STUDY_SERVER_APIS } from '../constant/api.constants';
import type { ApiEnvelope } from '../http/api-envelope';
import { MentorApiService } from '../http/mentor-api.service';

function authEnvelope(role = 'MENTOR'): ApiEnvelope<unknown> {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Signed in.',
    data: {
      full_name: 'Mentor Example',
      email: 'mentor@example.test',
      role,
      access_token: 'mentor-access-token',
      refresh_token: 'mentor-refresh-token',
      token_type: 'Bearer',
      expires_in: 3600,
      refresh_expires_in: 7200,
    },
    meta: {},
    traceId: 'trace-mentor',
  };
}

describe('MentorSessionService', () => {
  let http: HttpTestingController;
  let session: MentorSessionService;
  let api: MentorApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    http = TestBed.inject(HttpTestingController);
    session = TestBed.inject(MentorSessionService);
    api = TestBed.inject(MentorApiService);
  });

  afterEach(() => http.verify());

  it('accepts a Mentor login and attaches its Bearer token to protected API requests', async () => {
    const login = firstValueFrom(session.login('mentor@example.test', 'password'));
    http.expectOne('/api/v1/auth/login').flush(authEnvelope());
    await login;
    expect(session.isAuthenticated()).toBe(true);
    expect(session.profile()?.full_name).toBe('Mentor Example');

    const request = firstValueFrom(api.request(STUDY_SERVER_APIS.API_046));
    const protectedRequest = http.expectOne('/api/v1/mentor/courses');
    expect(protectedRequest.request.headers.get('Authorization')).toBe('Bearer mentor-access-token');
    protectedRequest.flush({ success: true, businessCode: 'OK', message: 'OK', data: {}, meta: {}, traceId: 'trace' });
    await request;
  });

  it('rejects a non-Mentor role and sends no protected request without a session', async () => {
    const login = firstValueFrom(session.login('student@example.test', 'password'));
    http.expectOne('/api/v1/auth/login').flush(authEnvelope('STUDENT'));
    await expect(login).rejects.toMatchObject({ code: 'MENTOR_ROLE_REQUIRED' });
    expect(session.isAuthenticated()).toBe(false);

    const protectedCall = firstValueFrom(api.request(STUDY_SERVER_APIS.API_046));
    await expect(protectedCall).rejects.toMatchObject({ code: 'LOGIN_REQUIRED' });
    http.expectNone('/api/v1/mentor/courses');
  });

  it('clears the local session after a protected API returns 401', async () => {
    const login = firstValueFrom(session.login('mentor@example.test', 'password'));
    http.expectOne('/api/v1/auth/login').flush(authEnvelope());
    await login;

    const request = firstValueFrom(api.request(STUDY_SERVER_APIS.API_046));
    http.expectOne('/api/v1/mentor/courses').flush(
      { success: false, businessCode: 'DESIGN_AUTHENTICATION_REQUIRED', message: 'Expired.', data: null, meta: {}, traceId: 'trace' },
      { status: 401, statusText: 'Unauthorized' },
    );
    await expect(request).rejects.toMatchObject({ status: 401 });
    expect(session.isAuthenticated()).toBe(false);
  });
});
