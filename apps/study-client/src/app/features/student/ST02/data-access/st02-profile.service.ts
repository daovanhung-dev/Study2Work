import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentProfile } from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST02ProfileService {
  private readonly api = inject(StudentApiService);

  profile() {
    return this.api.request<StudentProfile>(STUDY_SERVER_APIS.API_004);
  }
}
