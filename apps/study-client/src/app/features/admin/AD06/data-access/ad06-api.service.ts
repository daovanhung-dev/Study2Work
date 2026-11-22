import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type {
  AdminCourse,
  AdminCourseCreateRequest,
  AdminPage,
  AdminUserProfile,
} from '../../admin-api.models';
import { adminQueryParams } from '../../admin-query-params';

@Injectable({ providedIn: 'root' })
export class AD06ApiService {
  private readonly api = inject(AdminApiService);

  getCourses(query: { status?: string; mentor?: string; page?: number } = {}) {
    return this.api.get<AdminPage<AdminCourse>>(STUDY_SERVER_APIS.API_073, {
      params: adminQueryParams(query),
    });
  }

  getActiveMentors(page: number) {
    return this.api.get<AdminPage<AdminUserProfile>>(STUDY_SERVER_APIS.API_068, {
      params: adminQueryParams({ role: 'MENTOR', status: 'ACTIVE', page }),
    });
  }

  createCourse(body: AdminCourseCreateRequest) {
    return this.api.post<AdminCourse>(STUDY_SERVER_APIS.API_104, { body });
  }
}
