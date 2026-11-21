import { Injectable, inject } from '@angular/core';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentCourseProgress } from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST21CourseProgressService {
  private readonly api = inject(StudentApiService);
  progress(courseId: string) {
    return this.api.request<StudentCourseProgress>(STUDY_SERVER_APIS.API_037, {
      pathParams: { course_id: courseId },
    });
  }
}
