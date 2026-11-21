import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorNotificationOperation } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME15NotificationStatusService {
  private readonly api = inject(MentorApiService);
  status(notificationId: string) {
    return this.api.request<MentorNotificationOperation>(STUDY_SERVER_APIS.API_064, {
      pathParams: { notification_id: notificationId },
    });
  }
}
