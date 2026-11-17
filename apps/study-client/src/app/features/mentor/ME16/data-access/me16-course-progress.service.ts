import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorCourseProgressRow, MentorPage } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME16CourseProgressService {
  private readonly api = inject(MentorApiService);
  progress(courseId: string) {
    return this.api.request<MentorPage<MentorCourseProgressRow>>(STUDY_SERVER_APIS.API_065, {
      pathParams: { course_id: courseId },
    });
  }
}
