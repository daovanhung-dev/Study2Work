import { HttpContextToken, HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, switchMap, throwError } from 'rxjs';

import { AuthSessionService } from './auth-session.service';
import { AccessFailureService } from '../../features/shared/SH05/data-access/SH-05-forbidden.service';

/** A screen with its own denied state may handle 403 without global SH-05 navigation. */
export const HANDLE_FORBIDDEN_LOCALLY = new HttpContextToken<boolean>(() => false);

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  if (!request.url.startsWith('/api/v1/') || /^\/api\/v1\/auth\/(login|register|refresh)/.test(request.url)) {
    return next(request);
  }

  const session = inject(AuthSessionService);
  const router = inject(Router);
  const accessFailure = inject(AccessFailureService);

  const showAccessFailure = (error: HttpErrorResponse) => {
    const returnUrl = router.url.startsWith('/student') ? router.url : undefined;
    const httpError = accessFailure.fromHttpError(error, returnUrl);
    if (error.status === 401) session.clear();
    void router.navigate(['/forbidden'], { state: { httpError } });
  };

  return session.ensureAccessToken().pipe(
    switchMap((token) => {
      const authorized = token
        ? request.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
        : request;
      return next(authorized).pipe(
        catchError((error: unknown) => {
          if (error instanceof HttpErrorResponse && error.status === 403) {
            if (!request.context.get(HANDLE_FORBIDDEN_LOCALLY)) showAccessFailure(error);
            return throwError(() => error);
          }
          if (!(error instanceof HttpErrorResponse) || error.status !== 401 || !token) {
            return throwError(() => error);
          }
          return session.ensureAccessToken(true).pipe(
            switchMap((renewedToken) => {
              if (!renewedToken) {
                showAccessFailure(error);
                return throwError(() => error);
              }
              return next(request.clone({ setHeaders: { Authorization: `Bearer ${renewedToken}` } })).pipe(
                catchError((retryError: unknown) => {
                  if (retryError instanceof HttpErrorResponse && (retryError.status === 401 || retryError.status === 403)) {
                    if (retryError.status === 401 || !request.context.get(HANDLE_FORBIDDEN_LOCALLY)) showAccessFailure(retryError);
                  }
                  return throwError(() => retryError);
                }),
              );
            }),
          );
        }),
      );
    }),
  );
};
