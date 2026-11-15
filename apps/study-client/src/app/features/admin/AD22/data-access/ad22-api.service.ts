import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminDiscussion, AdminPage } from '../../admin-api.models';
import { adminQueryParams } from '../../admin-query-params';

@Injectable({ providedIn: 'root' })
export class AD22ApiService {
  private readonly api = inject(AdminApiService);

  getReportedDiscussions(query: { reason?: string; severity?: string; page?: number } = {}) {
    return this.api.get<AdminPage<AdminDiscussion>>(STUDY_SERVER_APIS.API_097, {
      params: adminQueryParams(query),
    });
  }
}
