import type { HttpResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { SH03RegistrationRequest } from '../models/sh03-registration.models';

@Injectable({ providedIn: 'root' })
export class SH03RegistrationService {
  private readonly studyApi = inject(StudyApiService);

  register(request: SH03RegistrationRequest): Observable<HttpResponse<ApiEnvelope<unknown>>> {
    return this.studyApi.requestWithResponse<unknown>(STUDY_SERVER_APIS.API_001, {
      body: request,
    });
  }
}
