import { Injectable, inject } from '@angular/core';
import { map } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminNotification, AdminPage } from '../../admin-api.models';
import { adminQueryParams } from '../../admin-query-params';
import { isAD19NotificationsEnvelope } from '../models/ad19-notifications.models';

@Injectable({ providedIn: 'root' })
export class AD19ApiService {
  private readonly api = inject(AdminApiService);

  getNotifications(query: { status?: string; channel?: string; page?: number } = {}) {
    return this.api
      .get<AdminPage<AdminNotification>>(STUDY_SERVER_APIS.API_092, {
        params: adminQueryParams(query),
      })
      .pipe(
        map((response) => {
          const candidate: unknown = response;
          if (!isAD19NotificationsEnvelope(candidate, query)) {
            throw new Error('API #92 returned an invalid notification page.');
          }
          return response;
        }),
      );
  }
}
