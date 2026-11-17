import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorContent, MentorCourse, MentorPage, MentorCourseProgressRow } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME03WorkspaceService {
  private readonly api = inject(MentorApiService);
  courses() {
    return this.api.request<MentorPage<MentorCourse>>(STUDY_SERVER_APIS.API_046);
  }
  content(courseId: string) {
    return this.api.request<MentorContent[]>(STUDY_SERVER_APIS.API_049, { pathParams: { course_id: courseId } });
  }
  progress(courseId: string) {
    return this.api.request<MentorPage<MentorCourseProgressRow>>(STUDY_SERVER_APIS.API_065, { pathParams: { course_id: courseId } });
  }
}
