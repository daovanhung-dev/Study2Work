import { Injectable, inject } from '@angular/core';

import { StudentSessionService } from '../../../../core/auth/student-session.service';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudyApiService } from '../../../../core/http/study-api.service';
import { StudentApiService } from '../../../../core/http/student-api.service';

@Injectable({ providedIn: 'root' })
export class GS07ResourceService {
  private readonly session = inject(StudentSessionService);
  private readonly publicApi = inject(StudyApiService);
  private readonly studentApi = inject(StudentApiService);

  resource(resourceId: string) {
    const options = { pathParams: { resource_id: resourceId } };
    return this.session.isAuthenticated()
      ? this.studentApi.request<unknown>(STUDY_SERVER_APIS.API_012, options)
      : this.publicApi.request<unknown>(STUDY_SERVER_APIS.API_012, options);
  }
}
