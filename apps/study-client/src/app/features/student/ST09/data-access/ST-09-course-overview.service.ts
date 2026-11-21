import { Injectable, inject } from '@angular/core';
import { StudyApiService } from '../../../../core/http/study-api.service';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { CourseLesson, CourseProgress } from '../models/ST-09-course-overview.models';

@Injectable({ providedIn: 'root' })
export class StudentCourseOverviewService {
  private readonly api = inject(StudyApiService);

  getProgress(courseId: string) {
    return this.api.request<CourseProgress>(STUDY_SERVER_APIS.API_037, {
      pathParams: {course_id: courseId},
    });
  }

  getCurriculum(courseId: string) {
    return this.api.request<{items: CourseLesson[]}>(STUDY_SERVER_APIS.API_009, {
      pathParams: {course_id: courseId},
    });
  }
}
