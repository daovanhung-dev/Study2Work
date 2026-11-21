import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminCourse, AdminPage, AdminQuiz } from '../../admin-api.models';
import { adminQueryParams } from '../../admin-query-params';

export interface CreateAdminQuizBody {
  readonly config: string;
  readonly questions: string;
}

@Injectable({ providedIn: 'root' })
export class AD16ApiService {
  private readonly api = inject(AdminApiService);

  getCourses(page: number) {
    return this.api.get<AdminPage<AdminCourse>>(STUDY_SERVER_APIS.API_073, {
      params: adminQueryParams({ page }),
    });
  }

  createQuiz(body: CreateAdminQuizBody) {
    return this.api.postWithResponse<AdminQuiz>(STUDY_SERVER_APIS.API_088, { body });
  }
}
