import { Injectable, inject } from '@angular/core';
import { HttpParams } from '@angular/common/http';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorCourse, MentorPage, MentorStudentSummary } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME13RecipientsService {
  private readonly api = inject(MentorApiService);
  courses(page = 1) {
    return this.api.request<MentorPage<MentorCourse>>(STUDY_SERVER_APIS.API_046, {
      params: new HttpParams().set('page', page).set('size', 100),
    });
  }
  students(courseId: string) {
    return this.api.request<MentorStudentSummary[]>(STUDY_SERVER_APIS.API_062, {
      pathParams: { course_id: courseId },
    });
  }
}
