import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminLesson } from '../../admin-api.models';

@Injectable({ providedIn: 'root' })
export class AD13ApiService {
  private readonly api = inject(AdminApiService);

  getLesson(lessonId: string) {
    return this.api.get<AdminLesson>(STUDY_SERVER_APIS.API_083, {
      pathParams: { lesson_id: lessonId },
    });
  }
}
