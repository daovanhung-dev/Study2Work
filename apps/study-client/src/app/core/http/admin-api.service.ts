import { HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import type { HttpResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, catchError, switchMap, throwError } from 'rxjs';

import { AdminSessionService } from '../auth/admin-session.service';
import type { StudyApiDescriptor } from '../constant/api.constants';
import type { ApiEnvelope } from './api-envelope';
import type { StudyApiRequestOptions } from './study-api.service';
import { StudyApiService } from './study-api.service';

@Injectable({ providedIn: 'root' })
export class AdminApiService {
  private readonly session = inject(AdminSessionService);
  private readonly studyApi = inject(StudyApiService);

  get<T>(api: StudyApiDescriptor, options: StudyApiRequestOptions = {}): Observable<ApiEnvelope<T>> {
    if (api.method !== 'GET' || api.status !== 'WIRED') {
      throw new Error(`Admin read requires a WIRED GET descriptor (API #${api.id}).`);
    }

    return this.withAdminAuthorization<T>(api, options);
  }

  post<T>(api: StudyApiDescriptor, options: StudyApiRequestOptions = {}): Observable<ApiEnvelope<T>> {
    if (api.method !== 'POST' || api.status !== 'WIRED' || !api.path.startsWith('/admin/')) {
      throw new Error(`Admin write requires a WIRED POST descriptor (API #${api.id}).`);
    }

    return this.withAdminAuthorization<T>(api, options);
  }

  postWithResponse<T>(
    api: StudyApiDescriptor,
    options: StudyApiRequestOptions = {},
  ): Observable<HttpResponse<ApiEnvelope<T>>> {
    if (api.method !== 'POST' || api.status !== 'WIRED' || !api.path.startsWith('/admin/')) {
      throw new Error(`Admin write requires a WIRED POST descriptor (API #${api.id}).`);
    }

    return this.withAdminAuthorizationResponse<T>(api, options);
  }

  private withAdminAuthorization<T>(
    api: StudyApiDescriptor,
    options: StudyApiRequestOptions,
  ): Observable<ApiEnvelope<T>> {
    return this.session.getAdminAccessToken().pipe(
      switchMap((token) => {
        const headers = (options.headers ?? new HttpHeaders()).set(
          'Authorization',
          `Bearer ${token}`,
        );
        return this.studyApi.request<T>(api, { ...options, headers });
      }),
      catchError((error: unknown) => {
        if (error instanceof HttpErrorResponse && error.status === 401) {
          this.session.endLocalSession();
        }
        return throwError(() => error);
      }),
    );
  }

  private withAdminAuthorizationResponse<T>(
    api: StudyApiDescriptor,
    options: StudyApiRequestOptions,
  ): Observable<HttpResponse<ApiEnvelope<T>>> {
    return this.session.getAdminAccessToken().pipe(
      switchMap((token) => {
        const headers = (options.headers ?? new HttpHeaders()).set(
          'Authorization',
          `Bearer ${token}`,
        );
        return this.studyApi.requestWithResponse<T>(api, { ...options, headers });
      }),
      catchError((error: unknown) => {
        if (error instanceof HttpErrorResponse && error.status === 401) {
          this.session.endLocalSession();
        }
        return throwError(() => error);
      }),
    );
  }
}
