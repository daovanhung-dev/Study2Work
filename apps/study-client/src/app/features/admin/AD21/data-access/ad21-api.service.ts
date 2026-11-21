import { Injectable, inject } from '@angular/core';
import { map } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminNotification } from '../../admin-api.models';
import { isAD21NotificationEnvelope } from '../models/ad21-notification.models';

@Injectable({ providedIn: 'root' })
export class AD21ApiService {
  private readonly api = inject(AdminApiService);

  getStatus(notificationId: string) {
    return this.api
      .get<AdminNotification>(STUDY_SERVER_APIS.API_096, {
        pathParams: { notification_id: notificationId },
      })
      .pipe(
        map((response) => {
          const candidate: unknown = response;
          if (!isAD21NotificationEnvelope(candidate, notificationId)) {
            throw new Error('API #96 returned a notification that does not match the route.');
          }
          return response;
        }),
      );
  }
}
