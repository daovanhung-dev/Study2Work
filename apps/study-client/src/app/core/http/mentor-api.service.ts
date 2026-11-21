import { HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, catchError, switchMap, throwError } from 'rxjs';

import { MentorSessionService } from '../auth/mentor-session.service';
import type { StudyApiDescriptor } from '../constant/api.constants';
import type { ApiEnvelope } from './api-envelope';
import type { StudyApiRequestOptions } from './study-api.service';
import { StudyApiService } from './study-api.service';

@Injectable({ providedIn: 'root' })
export class MentorApiService {
  private readonly session = inject(MentorSessionService);
  private readonly studyApi = inject(StudyApiService);

  request<T>(
    api: StudyApiDescriptor,
    options: StudyApiRequestOptions = {},
  ): Observable<ApiEnvelope<T>> {
    const isMentorRoute = api.path.startsWith('/mentor/');
    const isSharedMentorUpload = api.id === 34 && api.path === '/uploads';
    const isOwnedOperationRead =
      api.id === 18 && api.method === 'GET' && api.path === '/operations/{operation_id}';
    if (
      api.status !== 'WIRED' ||
      (!isMentorRoute && !isSharedMentorUpload && !isOwnedOperationRead)
    ) {
      throw new Error(`Mentor request requires a WIRED Mentor API descriptor (#${api.id}).`);
    }

    return this.session.getMentorAccessToken().pipe(
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
}
