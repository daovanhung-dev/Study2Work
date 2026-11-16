import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminNotification, AdminPage } from '../../admin-api.models';
import { adminQueryParams } from '../../admin-query-params';

@Injectable({ providedIn: 'root' })
export class AD19ApiService {
  private readonly api = inject(AdminApiService);

  getNotifications(query: { status?: string; channel?: string; page?: number } = {}) {
    return this.api.get<AdminPage<AdminNotification>>(STUDY_SERVER_APIS.API_092, {
      params: adminQueryParams(query),
    });
  }
}
