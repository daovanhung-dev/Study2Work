import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorNotificationOperation } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME14NotificationCreateService {
  private readonly api = inject(MentorApiService);
  create(recipients: string, title: string, content: number, channels: string) {
    return this.api.request<MentorNotificationOperation>(STUDY_SERVER_APIS.API_063, {
      body: { recipients, title, content, channels },
    });
  }
}
