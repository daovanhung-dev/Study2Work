import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorStudentProgress } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME17StudentProgressService {
  private readonly api = inject(MentorApiService);
  progress(courseId: string, studentId: string) {
    return this.api.request<MentorStudentProgress>(STUDY_SERVER_APIS.API_067, {
      pathParams: { course_id: courseId, student_id: studentId },
    });
  }
}
