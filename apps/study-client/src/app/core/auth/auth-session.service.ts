import { HttpClient } from '@angular/common/http';
import { computed, Injectable, inject, signal } from '@angular/core';
import { catchError, finalize, map, Observable, of, shareReplay } from 'rxjs';

import type { ApiEnvelope } from '../http/api-envelope';

const STORAGE_KEY = 'study.auth.session';
const EXPIRY_MARGIN_MS = 15_000;

interface AuthPayload {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  refresh_expires_in: number;
  role: string;
  full_name: string;
}

interface StoredSession {
  accessToken: string;
  refreshToken: string;
  accessExpiresAt: number;
  refreshExpiresAt: number;
  role: string;
  fullName: string;
}

@Injectable({ providedIn: 'root' })
export class AuthSessionService {
  private readonly http = inject(HttpClient);
  private readonly current = signal<StoredSession | null>(this.restore());
  private refreshing$: Observable<string | null> | null = null;

  readonly fullName = computed(() => this.current()?.fullName ?? 'Học viên');
  readonly role = computed(() => this.current()?.role ?? null);

  setSession(value: unknown): boolean {
    if (!isAuthPayload(value)) return false;

    const now = Date.now();
    const session: StoredSession = {
      accessToken: value.access_token,
      refreshToken: value.refresh_token,
      accessExpiresAt: now + value.expires_in * 1000,
      refreshExpiresAt: now + value.refresh_expires_in * 1000,
      role: value.role.toUpperCase(),
      fullName: value.full_name,
    };
    this.current.set(session);
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(session));
    } catch {
      // The in-memory session still works when browser storage is unavailable.
    }
    return true;
  }

  ensureAccessToken(forceRefresh = false): Observable<string | null> {
    const session = this.current();
    if (!session) return of(null);
    if (!forceRefresh && session.accessExpiresAt > Date.now() + EXPIRY_MARGIN_MS) {
      return of(session.accessToken);
    }
    if (session.refreshExpiresAt <= Date.now()) {
      this.clear();
      return of(null);
    }
    if (this.refreshing$) return this.refreshing$;

    this.refreshing$ = this.http
      .post<ApiEnvelope<AuthPayload>>('/api/v1/auth/refresh', {
        refresh_token: session.refreshToken,
      })
      .pipe(
        map((response) => {
          if (this.current()?.refreshToken !== session.refreshToken) return null;
          if (response.success && this.setSession(response.data)) {
            return this.current()!.accessToken;
          }
          this.clear();
          return null;
        }),
        catchError(() => {
          if (this.current()?.refreshToken === session.refreshToken) this.clear();
          return of(null);
        }),
        finalize(() => { this.refreshing$ = null; }),
        shareReplay(1),
      );
    return this.refreshing$;
  }

  clear(): void {
    this.current.set(null);
    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch {
      // The in-memory session has already been cleared.
    }
  }

  private restore(): StoredSession | null {
    try {
      const raw = sessionStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      const value: unknown = JSON.parse(raw);
      if (!isStoredSession(value) || value.refreshExpiresAt <= Date.now()) {
        sessionStorage.removeItem(STORAGE_KEY);
        return null;
      }
      return value;
    } catch {
      return null;
    }
  }
}

function isAuthPayload(value: unknown): value is AuthPayload {
  if (!value || typeof value !== 'object') return false;
  const data = value as Partial<AuthPayload>;
  return (
    typeof data.access_token === 'string' && data.access_token.length > 0 &&
    typeof data.refresh_token === 'string' && data.refresh_token.length > 0 &&
    data.token_type?.toLowerCase() === 'bearer' &&
    typeof data.expires_in === 'number' && Number.isFinite(data.expires_in) && data.expires_in > 0 &&
    typeof data.refresh_expires_in === 'number' && Number.isFinite(data.refresh_expires_in) && data.refresh_expires_in > 0 &&
    typeof data.role === 'string' && data.role.length > 0 &&
    typeof data.full_name === 'string'
  );
}

function isStoredSession(value: unknown): value is StoredSession {
  if (!value || typeof value !== 'object') return false;
  const session = value as Partial<StoredSession>;
  return (
    typeof session.accessToken === 'string' && session.accessToken.length > 0 &&
    typeof session.refreshToken === 'string' && session.refreshToken.length > 0 &&
    typeof session.accessExpiresAt === 'number' && Number.isFinite(session.accessExpiresAt) &&
    typeof session.refreshExpiresAt === 'number' && Number.isFinite(session.refreshExpiresAt) &&
    typeof session.role === 'string' &&
    typeof session.fullName === 'string'
  );
}
