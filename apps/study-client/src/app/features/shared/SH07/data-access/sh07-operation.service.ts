import { Injectable, inject } from '@angular/core';
import { Observable, throwError } from 'rxjs';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import { MentorSessionService } from '../../../../core/auth/mentor-session.service';
import { StudentSessionService } from '../../../../core/auth/student-session.service';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import { StudentApiService } from '../../../../core/http/student-api.service';

export class SH07AuthenticationRequiredError extends Error {
  constructor() {
    super('LOGIN_REQUIRED');
    this.name = 'SH07AuthenticationRequiredError';
  }
}

@Injectable({ providedIn: 'root' })
export class SH07OperationService {
  private readonly studentSession = inject(StudentSessionService);
  private readonly mentorSession = inject(MentorSessionService);
  private readonly adminSession = inject(AdminSessionService);
  private readonly studentApi = inject(StudentApiService);
  private readonly mentorApi = inject(MentorApiService);
  private readonly adminApi = inject(AdminApiService);

  getOperation(operationId: string): Observable<ApiEnvelope<unknown>> {
    const options = { pathParams: { operation_id: operationId } };
    const api = STUDY_SERVER_APIS.API_018;

    if (this.studentSession.isAuthenticated()) return this.studentApi.request(api, options);
    if (this.mentorSession.isAuthenticated()) return this.mentorApi.request(api, options);
    if (this.adminSession.isAuthenticated()) return this.adminApi.get(api, options);
    return throwError(() => new SH07AuthenticationRequiredError());
  }
}
