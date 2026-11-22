import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminCreateUserRequest, AdminPage, AdminUserProfile } from '../../admin-api.models';
import { adminQueryParams } from '../../admin-query-params';

@Injectable({ providedIn: 'root' })
export class AD02ApiService {
  private readonly api = inject(AdminApiService);

  getUsers(query: { role?: string; status?: string; keyword?: string; page?: number } = {}) {
    return this.api.get<AdminPage<AdminUserProfile>>(STUDY_SERVER_APIS.API_068, {
      params: adminQueryParams(query),
    });
  }

  createUser(body: AdminCreateUserRequest) {
    return this.api.post<AdminUserProfile>(STUDY_SERVER_APIS.API_105, { body });
  }
}
