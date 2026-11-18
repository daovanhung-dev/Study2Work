import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { AuthSessionService } from './auth-session.service';

const payload = {
  access_token: 'access-1', refresh_token: 'refresh-1', token_type: 'bearer',
  expires_in: 60, refresh_expires_in: 3600, role: 'STUDENT', full_name: 'QA Student',
};

describe('Study auth session', () => {
  let session: AuthSessionService;
  let http: HttpTestingController;

  beforeEach(() => {
    sessionStorage.clear();
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    session = TestBed.inject(AuthSessionService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    http.verify();
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it('stores a valid session and clears it on logout', async () => {
    expect(session.setSession(payload)).toBe(true);
    expect(session.role()).toBe('STUDENT');
    expect(session.fullName()).toBe('QA Student');
    await expect(firstValueFrom(session.ensureAccessToken())).resolves.toBe('access-1');
    expect(sessionStorage.getItem('study.auth.session')).not.toBeNull();

    session.clear();
    expect(session.role()).toBeNull();
    expect(sessionStorage.getItem('study.auth.session')).toBeNull();
  });

  it('refreshes an expired access token and replaces both tokens', async () => {
    const now = Date.now();
    vi.spyOn(Date, 'now').mockReturnValue(now);
    expect(session.setSession({ ...payload, expires_in: 1 })).toBe(true);
    vi.spyOn(Date, 'now').mockReturnValue(now + 20_000);
    const token = firstValueFrom(session.ensureAccessToken());
    const request = http.expectOne('/api/v1/auth/refresh');
    expect(request.request.body).toEqual({ refresh_token: 'refresh-1' });
    request.flush({ success: true, data: { ...payload, access_token: 'access-2', refresh_token: 'refresh-2' } });
    await expect(token).resolves.toBe('access-2');
    await expect(firstValueFrom(session.ensureAccessToken())).resolves.toBe('access-2');
  });

  it('does not restore a session when logout occurs during refresh', async () => {
    expect(session.setSession(payload)).toBe(true);
    const token = firstValueFrom(session.ensureAccessToken(true));
    const request = http.expectOne('/api/v1/auth/refresh');
    session.clear();
    request.flush({ success: true, data: { ...payload, access_token: 'access-2' } });
    await expect(token).resolves.toBeNull();
    expect(session.role()).toBeNull();
  });

  it('clears the session when refresh is rejected', async () => {
    expect(session.setSession({ ...payload, expires_in: 1 })).toBe(true);
    const token = firstValueFrom(session.ensureAccessToken(true));
    http.expectOne('/api/v1/auth/refresh').flush({}, { status: 401, statusText: 'Unauthorized' });
    await expect(token).resolves.toBeNull();
    expect(session.role()).toBeNull();
  });
});
