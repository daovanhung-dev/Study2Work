import { Injectable, inject } from '@angular/core';

import { StudyApiService } from '../../../../core/http/study-api.service';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { LoginCredentials } from '../models/SH-02-login.models';

@Injectable({ providedIn: 'root' })
export class LoginApi {
  private readonly api = inject(StudyApiService);

  login(credentials: LoginCredentials) {
    return this.api.request<unknown>(STUDY_SERVER_APIS.API_003, {
      body: credentials,
    });
  }
}
