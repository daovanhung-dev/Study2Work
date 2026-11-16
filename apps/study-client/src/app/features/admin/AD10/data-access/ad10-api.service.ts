import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminContent, AdminPage } from '../../admin-api.models';
import { adminQueryParams } from '../../admin-query-params';

@Injectable({ providedIn: 'root' })
export class AD10ApiService {
  private readonly api = inject(AdminApiService);

  getPendingContent(query: { type?: string; course?: string; page?: number } = {}) {
    return this.api.get<AdminPage<AdminContent>>(STUDY_SERVER_APIS.API_078, {
      params: adminQueryParams(query),
    });
  }
}
