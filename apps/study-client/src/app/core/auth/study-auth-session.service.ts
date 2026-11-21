import { Injectable, inject, signal } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { Observable, catchError, finalize, map, shareReplay, tap, throwError } from 'rxjs';

import { STUDY_SERVER_APIS } from '../constant/api.constants';
import { StudyApiService } from '../http/study-api.service';
import type { StudyAuthPayload } from './study-auth.models';

const SESSION_CHANNEL = 'study-auth-session';
const SESSION_STORAGE_EVENT = 'study-auth-session-event';

@Injectable({ providedIn: 'root' })
export class StudyAuthSessionService {
  private readonly api = inject(StudyApiService);
  private refreshRequest: Observable<string> | null = null;
  private channel: BroadcastChannel | null = null;
  private profileVerified = false;

  readonly accessToken = signal<string | null>(null);

  constructor() {
    if (typeof window === 'undefined') return;

    if (typeof BroadcastChannel !== 'undefined') {
      this.channel = new BroadcastChannel(SESSION_CHANNEL);
      this.channel.addEventListener('message', (event: MessageEvent<unknown>) => {
        if (event.data === 'session-changed') this.reloadForSessionChange();
      });
      return;
    }

    window.addEventListener('storage', (event: StorageEvent) => {
      if (event.key === SESSION_STORAGE_EVENT) this.reloadForSessionChange();
    });
  }

  isStudentProfileVerified(): boolean {
    return this.profileVerified && this.accessToken() !== null;
  }

  setAccessToken(token: string): void {
    this.accessToken.set(token);
    this.profileVerified = false;
  }

  markStudentProfileVerified(): void {
    this.profileVerified = true;
  }

  clearAccessToken(): void {
    this.accessToken.set(null);
    this.profileVerified = false;
  }

  refreshAccessToken(): Observable<string> {
    if (this.refreshRequest) return this.refreshRequest;

    this.refreshRequest = this.api
      .requestDeclared<StudyAuthPayload>(STUDY_SERVER_APIS.API_003_REFRESH, {
        withCredentials: true,
      })
      .pipe(
        map((response) => {
          const token = response?.success === true ? response.data?.access_token : null;
          if (typeof token !== 'string' || !token) {
            throw new Error('Invalid Study refresh response');
          }
          return token;
        }),
        tap((token) => this.setAccessToken(token)),
        catchError((error: unknown) => {
          this.clearAccessToken();
          return throwError(() => error);
        }),
        finalize(() => {
          this.refreshRequest = null;
        }),
        shareReplay({ bufferSize: 1, refCount: false }),
      );

    return this.refreshRequest;
  }

  logout(): Observable<void> {
    this.clearAccessToken();
    return this.api
      .requestDeclared<unknown>(STUDY_SERVER_APIS.API_003_LOGOUT, { withCredentials: true })
      .pipe(
        map(() => undefined),
        tap(() => this.broadcastSessionChange()),
        catchError((error: unknown) => {
          if (error instanceof HttpErrorResponse) this.clearAccessToken();
          return throwError(() => error);
        }),
      );
  }

  broadcastSessionChange(): void {
    if (this.channel) {
      this.channel.postMessage('session-changed');
      return;
    }

    try {
      window.localStorage.setItem(SESSION_STORAGE_EVENT, crypto.randomUUID());
      window.localStorage.removeItem(SESSION_STORAGE_EVENT);
    } catch {
      // Browser storage may be disabled; no credential is stored in this fallback.
    }
  }

  private reloadForSessionChange(): void {
    this.clearAccessToken();
    window.location.reload();
  }
}
