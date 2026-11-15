import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminNotification } from '../../admin-api.models';

@Injectable({ providedIn: 'root' })
export class AD21ApiService {
  private readonly api = inject(AdminApiService);

  getStatus(notificationId: string) {
    return this.api.get<AdminNotification>(STUDY_SERVER_APIS.API_096, {
      pathParams: { notification_id: notificationId },
    });
  }
}
