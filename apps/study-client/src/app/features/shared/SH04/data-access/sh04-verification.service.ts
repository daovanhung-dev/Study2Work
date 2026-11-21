import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudyApiService } from '../../../../core/http/study-api.service';

@Injectable({ providedIn: 'root' })
export class SH04VerificationService {
  private readonly api = inject(StudyApiService);

  sendRequest(userId: number, email: string) {
    return this.api.requestWithResponse<unknown>(STUDY_SERVER_APIS.API_002, {
      body: { user_id: userId, email },
    });
  }
}
