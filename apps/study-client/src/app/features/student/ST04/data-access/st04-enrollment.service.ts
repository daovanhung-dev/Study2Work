import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentEnrollment } from '../../shared/models/student-enrollment.models';
import type { StudentCourseSummary, StudentPage } from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST04EnrollmentService {
  private readonly api = inject(StudentApiService);

  enrollmentStatus(courseId: string) {
    return this.api.request<StudentEnrollment>(STUDY_SERVER_APIS.API_015, {
      pathParams: { course_id: courseId },
    });
  }

  enroll(courseId: number) {
    return this.api.request<StudentEnrollment>(STUDY_SERVER_APIS.API_019, {
      pathParams: { course_id: courseId },
      body: { course_id: courseId },
    });
  }

  courses() {
    return this.api.request<StudentPage<StudentCourseSummary>>(STUDY_SERVER_APIS.API_020, {
      params: new HttpParams().set('status', 'ACTIVE').set('page', 1),
    });
  }
}
