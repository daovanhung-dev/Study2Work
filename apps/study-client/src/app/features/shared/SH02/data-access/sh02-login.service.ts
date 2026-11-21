import { Injectable, inject } from '@angular/core';
import { Observable, catchError, map, of, switchMap, throwError } from 'rxjs';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import { MentorSessionService } from '../../../../core/auth/mentor-session.service';
import { StudentSessionService } from '../../../../core/auth/student-session.service';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { StudyApiService } from '../../../../core/http/study-api.service';

export type SH02LoginDestination = '/student' | '/mentor' | '/admin';

export type SH02LoginErrorCode =
  | 'INVALID_AUTH_RESPONSE'
  | 'UNSUPPORTED_ROLE'
  | 'STUDENT_PROFILE_MISMATCH';

export class SH02LoginError extends Error {
  constructor(readonly code: SH02LoginErrorCode) {
    super(code);
    this.name = 'SH02LoginError';
  }
}

@Injectable({ providedIn: 'root' })
export class SH02LoginService {
  private readonly studyApi = inject(StudyApiService);
  private readonly studentApi = inject(StudentApiService);
  private readonly studentSession = inject(StudentSessionService);
  private readonly mentorSession = inject(MentorSessionService);
  private readonly adminSession = inject(AdminSessionService);

  login(email: string, password: string): Observable<SH02LoginDestination> {
    return this.studyApi
      .requestWithResponse<unknown>(STUDY_SERVER_APIS.API_003, {
        body: { email, password },
      })
      .pipe(
        switchMap((response) => {
          const envelope = response.body;
          if (
            response.status !== 200 ||
            !isSuccessEnvelope(envelope, 'DESIGN_RESOURCE_RETRIEVED')
          ) {
            return throwError(() => new SH02LoginError('INVALID_AUTH_RESPONSE'));
          }

          const role = readSupportedRole(envelope.data);
          if (!role) return throwError(() => new SH02LoginError('UNSUPPORTED_ROLE'));

          this.endAllSessions();

          if (role === 'STUDENT') {
            this.studentSession.acceptLoginEnvelope(envelope);
            return this.verifyStudentProfile().pipe(
              map(() => '/student' as const),
              catchError((error: unknown) => {
                this.studentSession.endLocalSession();
                return throwError(() => error);
              }),
            );
          }

          if (role === 'MENTOR') {
            this.mentorSession.acceptLoginEnvelope(envelope);
            return of('/mentor' as const);
          }

          this.adminSession.acceptLoginEnvelope(envelope);
          return of('/admin' as const);
        }),
      );
  }

  private verifyStudentProfile(): Observable<void> {
    return this.studentApi.request<unknown>(STUDY_SERVER_APIS.API_004).pipe(
      map((envelope) => {
        const profile = asRecord(envelope.data);
        const currentSession = this.studentSession.profile();
        if (
          !isSuccessEnvelope(envelope, 'DESIGN_RESOURCE_RETRIEVED') ||
          !profile ||
          !currentSession ||
          typeof profile['email'] !== 'string' ||
          profile['email'].trim().toLowerCase() !== currentSession.email.trim().toLowerCase() ||
          typeof profile['role'] !== 'string' ||
          profile['role'].trim().toUpperCase() !== 'STUDENT'
        ) {
          throw new SH02LoginError('STUDENT_PROFILE_MISMATCH');
        }
      }),
    );
  }

  private endAllSessions(): void {
    this.studentSession.endLocalSession();
    this.mentorSession.endLocalSession();
    this.adminSession.endLocalSession();
  }
}

function isSuccessEnvelope(
  value: unknown,
  businessCode: string,
): value is ApiEnvelope<unknown> {
  const envelope = asRecord(value);
  if (!envelope) return false;
  return (
    envelope['success'] === true &&
    envelope['businessCode'] === businessCode &&
    typeof envelope['message'] === 'string' &&
    asRecord(envelope['meta']) !== null
  );
}

function readSupportedRole(value: unknown): 'STUDENT' | 'MENTOR' | 'ADMIN' | null {
  const data = asRecord(value);
  if (!data || typeof data['role'] !== 'string') return null;
  const role = data['role'].trim().toUpperCase();
  return role === 'STUDENT' || role === 'MENTOR' || role === 'ADMIN' ? role : null;
}

function asRecord(value: unknown): Record<string, unknown> | null {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : null;
}
