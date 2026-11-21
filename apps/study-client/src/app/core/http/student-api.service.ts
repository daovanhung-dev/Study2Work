import { HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, catchError, switchMap, throwError } from 'rxjs';

import { normalizeAuthorizationError } from '../auth/authorization-error';
import { StudentSessionService } from '../auth/student-session.service';
import type { StudyApiDescriptor } from '../constant/api.constants';
import { StudyApiService } from './study-api.service';
import type { StudyApiRequestOptions } from './study-api.service';
import type { ApiEnvelope } from './api-envelope';

@Injectable({ providedIn: 'root' })
export class StudentApiService {
  private readonly session = inject(StudentSessionService);
  private readonly studyApi = inject(StudyApiService);
  private readonly router = inject(Router);

  request<T>(
    api: StudyApiDescriptor,
    options: StudyApiRequestOptions = {},
  ): Observable<ApiEnvelope<T>> {
    return this.session.getStudentAccessToken().pipe(
      switchMap((token) => {
        return this.sendWithToken<T>(api, options, token).pipe(
          catchError((error: unknown) => {
            if (isCurrentUserRead(api) && isHttpStatus(error, 401)) {
              return this.session.refreshAfterUnauthorized().pipe(
                switchMap((refreshedToken) => this.sendWithToken<T>(api, options, refreshedToken)),
              );
            }
            return throwError(() => error);
          }),
        );
      }),
      catchError((error: unknown) => {
        if (error instanceof HttpErrorResponse) {
          if (error.status === 401) this.session.endLocalSession();

          if (
            isCurrentUserRead(api) &&
            (error.status === 401 || error.status === 403)
          ) {
            const state = normalizeAuthorizationError(error);
            if (state) {
              const returnTo = safeInternalReturnTo(this.router.url);
              void this.router.navigateByUrl('/forbidden', {
                state: { sh05Error: state, sh05ReturnTo: returnTo },
              });
            }
          }
        }
        return throwError(() => error);
      }),
    );
  }

  private sendWithToken<T>(
    api: StudyApiDescriptor,
    options: StudyApiRequestOptions,
    token: string,
  ): Observable<ApiEnvelope<T>> {
    const headers = (options.headers ?? new HttpHeaders()).set(
      'Authorization',
      `Bearer ${token}`,
    );
    return this.studyApi.request<T>(api, { ...options, headers });
  }
}

function isCurrentUserRead(api: StudyApiDescriptor): boolean {
  return api.id === 4 && api.method === 'GET' && api.path === '/users/me';
}

function isHttpStatus(error: unknown, status: number): error is HttpErrorResponse {
  return error instanceof HttpErrorResponse && error.status === status;
}

function safeInternalReturnTo(value: string): string {
  if (
    !value.startsWith('/') ||
    value.startsWith('//') ||
    value.includes('\\') ||
    /[\u0000-\u001f]/.test(value)
  ) {
    return '/';
  }
  return value;
}
