import { Injectable, inject } from '@angular/core';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentAchievement, StudentPage } from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST22AchievementsService {
  private readonly api = inject(StudentApiService);
  achievements() {
    return this.api.request<StudentPage<StudentAchievement>>(STUDY_SERVER_APIS.API_038);
  }
}
