import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type {
  StudentCourseProgress,
  StudentCourseSummary,
  StudentPage,
} from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST09CourseOverviewService {
  private readonly api = inject(StudentApiService);

  activeCourses(page: number) {
    const params = new HttpParams().set('status', 'ACTIVE').set('page', page);
    return this.api.request<StudentPage<StudentCourseSummary>>(STUDY_SERVER_APIS.API_020, {
      params,
    });
  }

  progress(courseId: string) {
    return this.api.request<StudentCourseProgress>(STUDY_SERVER_APIS.API_037, {
      pathParams: { course_id: courseId },
    });
  }
}
