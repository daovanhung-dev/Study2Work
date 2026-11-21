import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminPage, AdminQuiz } from '../../admin-api.models';
import { adminQueryParams } from '../../admin-query-params';

@Injectable({ providedIn: 'root' })
export class AD15ApiService {
  private readonly api = inject(AdminApiService);

  getQuizzes(query: { course?: string; status?: string; page?: number } = {}) {
    return this.api.get<AdminPage<AdminQuiz>>(STUDY_SERVER_APIS.API_087, {
      params: adminQueryParams(query),
    });
  }
}
