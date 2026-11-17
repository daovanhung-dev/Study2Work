import { HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, catchError, switchMap, throwError } from 'rxjs';

import { StudentSessionService } from '../auth/student-session.service';
import type { StudyApiDescriptor } from '../constant/api.constants';
import { StudyApiService } from './study-api.service';
import type { StudyApiRequestOptions } from './study-api.service';
import type { ApiEnvelope } from './api-envelope';

@Injectable({ providedIn: 'root' })
export class StudentApiService {
  private readonly session = inject(StudentSessionService);
  private readonly studyApi = inject(StudyApiService);

  request<T>(
    api: StudyApiDescriptor,
    options: StudyApiRequestOptions = {},
  ): Observable<ApiEnvelope<T>> {
    return this.session.getStudentAccessToken().pipe(
      switchMap((token) => {
        const headers = (options.headers ?? new HttpHeaders()).set(
          'Authorization',
          `Bearer ${token}`,
        );
        return this.studyApi.request<T>(api, { ...options, headers });
      }),
      catchError((error: unknown) => {
        if (error instanceof HttpErrorResponse && error.status === 401)
          this.session.endLocalSession();
        return throwError(() => error);
      }),
    );
  }
}
