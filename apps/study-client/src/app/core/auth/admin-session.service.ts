import { Injectable, computed, inject, signal } from '@angular/core';
import { Observable, catchError, finalize, map, of, shareReplay, throwError } from 'rxjs';

import { STUDY_SERVER_APIS } from '../constant/api.constants';
import { StudyApiService } from '../http/study-api.service';
import type { ApiEnvelope } from '../http/api-envelope';

export interface AdminSessionProfile {
  readonly full_name: string;
  readonly email: string;
  readonly role: string;
}

export type AdminSessionErrorCode =
  | 'ADMIN_ROLE_REQUIRED'
  | 'INVALID_AUTH_RESPONSE'
  | 'LOGIN_REQUIRED';

export class AdminSessionError extends Error {
  constructor(readonly code: AdminSessionErrorCode) {
    super(code);
    this.name = 'AdminSessionError';
  }
}

interface AuthPayload extends AdminSessionProfile {
  readonly access_token: string;
  readonly refresh_token: string;
  readonly token_type: string;
  readonly expires_in: number;
  readonly refresh_expires_in: number;
}

@Injectable({ providedIn: 'root' })
export class AdminSessionService {
  private readonly studyApi = inject(StudyApiService);
  private readonly profileState = signal<AdminSessionProfile | null>(null);
  private accessToken: string | null = null;
  private refreshToken: string | null = null;
  private accessTokenExpiresAt = 0;
  private refreshRequest: Observable<void> | null = null;

  readonly profile = this.profileState.asReadonly();
  readonly isAuthenticated = computed(() => {
    const profile = this.profileState();
    return !!this.accessToken && profile !== null && isAdminRole(profile.role);
  });

  login(email: string, password: string): Observable<void> {
    return this.studyApi
      .request<unknown>(STUDY_SERVER_APIS.API_003, { body: { email, password } })
      .pipe(
        map((envelope) => {
          this.acceptEnvelope(envelope);
        }),
      );
  }

  getAdminAccessToken(): Observable<string> {
    if (!this.isAuthenticated() || !this.accessToken || !this.refreshToken) {
      return throwError(() => new AdminSessionError('LOGIN_REQUIRED'));
    }

    if (Date.now() < this.accessTokenExpiresAt) {
      return of(this.accessToken);
    }

    return this.refreshAccessToken();
  }

  endLocalSession(): void {
    this.accessToken = null;
    this.refreshToken = null;
    this.accessTokenExpiresAt = 0;
    this.refreshRequest = null;
    this.profileState.set(null);
  }

  private refreshAccessToken(): Observable<string> {
    if (!this.refreshToken) {
      this.endLocalSession();
      return throwError(() => new AdminSessionError('LOGIN_REQUIRED'));
    }

    if (!this.refreshRequest) {
      this.refreshRequest = this.studyApi
        .request<unknown>(STUDY_SERVER_APIS.API_003_REFRESH, {
          body: { refresh_token: this.refreshToken },
        })
        .pipe(
          map((envelope) => {
            this.acceptEnvelope(envelope);
          }),
          catchError((error: unknown) => {
            this.endLocalSession();
            return throwError(() => error);
          }),
          finalize(() => {
            this.refreshRequest = null;
          }),
          shareReplay({ bufferSize: 1, refCount: false }),
        );
    }

    return this.refreshRequest.pipe(
      map(() => {
        if (!this.accessToken || !this.isAuthenticated()) {
          throw new AdminSessionError('LOGIN_REQUIRED');
        }
        return this.accessToken;
      }),
    );
  }

  private acceptEnvelope(envelope: ApiEnvelope<unknown>): void {
    const payload = envelope.success ? parseAuthPayload(envelope.data) : null;
    if (!payload) {
      throw new AdminSessionError('INVALID_AUTH_RESPONSE');
    }
    if (!isAdminRole(payload.role)) {
      this.endLocalSession();
      throw new AdminSessionError('ADMIN_ROLE_REQUIRED');
    }

    this.accessToken = payload.access_token;
    this.refreshToken = payload.refresh_token;
    this.accessTokenExpiresAt = Date.now() + payload.expires_in * 1000;
    this.profileState.set({
      full_name: payload.full_name,
      email: payload.email,
      role: payload.role,
    });
  }
}

function parseAuthPayload(value: unknown): AuthPayload | null {
  if (!value || typeof value !== 'object') {
    return null;
  }

  const candidate = value as Record<string, unknown>;
  if (
    typeof candidate['full_name'] !== 'string'
    || typeof candidate['email'] !== 'string'
    || typeof candidate['role'] !== 'string'
    || typeof candidate['access_token'] !== 'string'
    || typeof candidate['refresh_token'] !== 'string'
    || typeof candidate['token_type'] !== 'string'
    || candidate['token_type'].toLowerCase() !== 'bearer'
    || typeof candidate['expires_in'] !== 'number'
    || candidate['expires_in'] <= 0
    || typeof candidate['refresh_expires_in'] !== 'number'
    || candidate['refresh_expires_in'] <= 0
  ) {
    return null;
  }

  return candidate as unknown as AuthPayload;
}

function isAdminRole(role: string): boolean {
  return role.trim().toUpperCase() === 'ADMIN';
}
