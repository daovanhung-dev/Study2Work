import { Injectable, inject } from '@angular/core';

import { StudyApiService } from '../../../../core/http/study-api.service';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { CreatedUser, RegistrationRequest } from '../models/SH-03-register.models';

@Injectable({ providedIn: 'root' })
export class RegisterApi {
  private readonly api = inject(StudyApiService);

  register(request: RegistrationRequest) {
    return this.api.requestResponse<CreatedUser>(STUDY_SERVER_APIS.API_001, {
      body: request,
    });
  }
}
