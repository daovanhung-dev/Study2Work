import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorCourseAnalytics } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME18AnalyticsService {
  private readonly api = inject(MentorApiService);
  load(courseId: string) {
    return this.api.request<MentorCourseAnalytics>(STUDY_SERVER_APIS.API_066, {
      pathParams: { course_id: courseId },
    });
  }
}
