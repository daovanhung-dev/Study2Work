import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { StudentNotificationsService } from '../../shared/data-access/student-notifications.service';
import type {
  StudentAchievement,
  StudentCourseSummary,
  StudentPage,
} from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST01OverviewService {
  private readonly api = inject(StudentApiService);
  private readonly notificationsApi = inject(StudentNotificationsService);

  activeCourses() {
    const params = new HttpParams().set('status', 'ACTIVE').set('page', 1);
    return this.api.request<StudentPage<StudentCourseSummary>>(STUDY_SERVER_APIS.API_020, {
      params,
    });
  }

  achievements() {
    return this.api.request<StudentPage<StudentAchievement>>(STUDY_SERVER_APIS.API_038);
  }

  unreadNotifications() {
    return this.notificationsApi.list(true, 1);
  }
}
