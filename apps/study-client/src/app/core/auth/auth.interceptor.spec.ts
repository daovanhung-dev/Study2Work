import { HttpClient, HttpContext, provideHttpClient, withInterceptors } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { authInterceptor, HANDLE_FORBIDDEN_LOCALLY } from './auth.interceptor';
import { AuthSessionService } from './auth-session.service';

const payload = {
  access_token: 'access-1', refresh_token: 'refresh-1', token_type: 'bearer',
  expires_in: 60, refresh_expires_in: 3600, role: 'STUDENT', full_name: 'QA Student',
};

describe('Study auth interceptor', () => {
  let client: HttpClient;
  let http: HttpTestingController;
  let session: AuthSessionService;

  beforeEach(() => {
    sessionStorage.clear();
    TestBed.configureTestingModule({
      providers: [provideRouter([]), provideHttpClient(withInterceptors([authInterceptor])), provideHttpClientTesting()],
    });
    client = TestBed.inject(HttpClient);
    http = TestBed.inject(HttpTestingController);
    session = TestBed.inject(AuthSessionService);
  });

  afterEach(() => { http.verify(); sessionStorage.clear(); });

  it('attaches Bearer token to a protected API request', async () => {
    session.setSession(payload);
    const response = firstValueFrom(client.get('/api/v1/users/me'));
    const request = http.expectOne('/api/v1/users/me');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-1');
    request.flush({ success: true });
    await expect(response).resolves.toEqual({ success: true });
  });

  it('refreshes and retries a request after a 401', async () => {
    session.setSession(payload);
    const response = firstValueFrom(client.get('/api/v1/users/me'));
    http.expectOne('/api/v1/users/me').flush({}, { status: 401, statusText: 'Unauthorized' });
    const refresh = http.expectOne('/api/v1/auth/refresh');
    expect(refresh.request.headers.has('Authorization')).toBe(false);
    refresh.flush({ success: true, data: { ...payload, access_token: 'access-2', refresh_token: 'refresh-2' } });
    const retry = http.expectOne('/api/v1/users/me');
    expect(retry.request.headers.get('Authorization')).toBe('Bearer access-2');
    retry.flush({ success: true });
    await expect(response).resolves.toEqual({ success: true });
  });

  it('lets a screen handle its own 403 without redirecting to SH-05', async () => {
    session.setSession(payload);
    const router = TestBed.inject(Router);
    const response = firstValueFrom(client.get('/api/v1/lessons/1/access', {
      context: new HttpContext().set(HANDLE_FORBIDDEN_LOCALLY, true),
    }));
    http.expectOne('/api/v1/lessons/1/access').flush({}, { status: 403, statusText: 'Forbidden' });
    await expect(response).rejects.toMatchObject({ status: 403 });
    expect(router.url).toBe('/');
  });
});
