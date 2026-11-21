import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { SH02LoginService } from './sh02-login.service';

describe('SH02LoginService', () => {
  let service: SH02LoginService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    });
    service = TestBed.inject(SH02LoginService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('uses the current HTTP 200 profile/token contract and verifies a Student with API #04', async () => {
    const login = firstValueFrom(service.login('student@example.test', ' exact password '));
    const request = http.expectOne('/api/v1/auth/login');
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual({ email: 'student@example.test', password: ' exact password ' });
    request.flush(successEnvelope(authPayload('STUDENT')), { status: 200, statusText: 'OK' });

    const profile = http.expectOne('/api/v1/users/me');
    expect(profile.request.method).toBe('GET');
    expect(profile.request.headers.get('Authorization')).toBe('Bearer access-token');
    profile.flush(successEnvelope({ email: 'student@example.test', role: 'STUDENT' }));

    await expect(login).resolves.toBe('/student');
    http.expectNone('/api/v1/auth/refresh');
  });

  it('routes Mentor and Admin to their role home without a returnTo parameter or Student profile request', async () => {
    const mentorLogin = firstValueFrom(service.login('mentor@example.test', 'password'));
    http.expectOne('/api/v1/auth/login').flush(successEnvelope(authPayload('MENTOR')), {
      status: 200,
      statusText: 'OK',
    });
    await expect(mentorLogin).resolves.toBe('/mentor');
    http.expectNone('/api/v1/users/me');

    const adminLogin = firstValueFrom(service.login('admin@example.test', 'password'));
    http.expectOne('/api/v1/auth/login').flush(successEnvelope(authPayload('ADMIN')), {
      status: 200,
      statusText: 'OK',
    });
    await expect(adminLogin).resolves.toBe('/admin');
    http.expectNone('/api/v1/users/me');
  });

  it('rejects an unexpected success status instead of treating it as an authenticated session', async () => {
    const login = firstValueFrom(service.login('student@example.test', 'password'));
    http.expectOne('/api/v1/auth/login').flush(successEnvelope(authPayload('STUDENT')), {
      status: 201,
      statusText: 'Created',
    });
    await expect(login).rejects.toMatchObject({ code: 'INVALID_AUTH_RESPONSE' });
    http.expectNone('/api/v1/users/me');
  });
});

function authPayload(role: string) {
  return {
    full_name: 'Test User',
    email: `${role.toLowerCase()}@example.test`,
    role,
    access_token: 'access-token',
    refresh_token: 'refresh-token',
    token_type: 'bearer',
    expires_in: 60,
    refresh_expires_in: 3600,
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
