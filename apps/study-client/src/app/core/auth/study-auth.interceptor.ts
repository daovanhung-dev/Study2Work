import {
  HttpContextToken,
  HttpErrorResponse,
  HttpInterceptorFn,
} from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, switchMap, throwError } from 'rxjs';

import { STUDY_API_BASE_PATH } from '../constant/api.constants';
import { StudyAuthSessionService } from './study-auth-session.service';

const AUTH_RETRY = new HttpContextToken<boolean>(() => false);

export const studyAuthInterceptor: HttpInterceptorFn = (request, next) => {
  if (!isStudyApiRequest(request.url) || isSessionEndpoint(request.url)) {
    return next(request);
  }

  const session = inject(StudyAuthSessionService);
  const token = session.accessToken();
  const authorizedRequest =
    token && !request.headers.has('Authorization')
      ? request.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
      : request;

  return next(authorizedRequest).pipe(
    catchError((error: unknown) => {
      if (
        !(error instanceof HttpErrorResponse) ||
        error.status !== 401 ||
        !authorizedRequest.headers.has('Authorization') ||
        authorizedRequest.context.get(AUTH_RETRY)
      ) {
        return throwError(() => error);
      }

      return session.refreshAccessToken().pipe(
        switchMap((freshToken) =>
          next(
            authorizedRequest.clone({
              setHeaders: { Authorization: `Bearer ${freshToken}` },
              context: authorizedRequest.context.set(AUTH_RETRY, true),
            }),
          ),
        ),
        catchError(() => {
          session.clearAccessToken();
          return throwError(() => error);
        }),
      );
    }),
  );
};

function isStudyApiRequest(url: string): boolean {
  if (typeof window === 'undefined') return false;
  try {
    const parsed = new URL(url, window.location.origin);
    return (
      parsed.origin === window.location.origin &&
      (parsed.pathname === STUDY_API_BASE_PATH ||
        parsed.pathname.startsWith(`${STUDY_API_BASE_PATH}/`))
    );
  } catch {
    return false;
  }
}

function isSessionEndpoint(url: string): boolean {
  return /\/auth\/(login|refresh|logout)(?:[?#]|$)/.test(url);
}
