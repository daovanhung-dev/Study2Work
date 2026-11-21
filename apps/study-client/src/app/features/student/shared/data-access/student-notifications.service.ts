import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type {
  StudentNotification,
  StudentNotificationReadSummary,
  StudentPage,
} from '../models/student-api.models';

@Injectable({ providedIn: 'root' })
export class StudentNotificationsService {
  private readonly api = inject(StudentApiService);

  list(unreadOnly: boolean, page: number) {
    const params = new HttpParams().set('unread_only', unreadOnly).set('page', page);
    return this.api.request<StudentPage<StudentNotification>>(STUDY_SERVER_APIS.API_043, {
      params,
    });
  }

  markRead(notificationId: string) {
    return this.api.request<StudentPage<StudentNotification>>(STUDY_SERVER_APIS.API_044, {
      pathParams: { notification_id: notificationId },
    });
  }

  markAllRead() {
    return this.api.request<StudentNotificationReadSummary>(STUDY_SERVER_APIS.API_045);
  }
}
