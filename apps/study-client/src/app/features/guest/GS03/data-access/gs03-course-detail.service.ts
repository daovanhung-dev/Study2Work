import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type { GuestPublicCoursePage } from '../../shared/models/guest-course.models';

@Injectable({ providedIn: 'root' })
export class GS03CourseDetailService {
  private readonly api = inject(StudyApiService);

  getCourse(courseId: string): Observable<ApiEnvelope<GuestPublicCoursePage>> {
    return this.api.request<GuestPublicCoursePage>(STUDY_SERVER_APIS.API_008, {
      pathParams: { course_id: courseId },
    });
  }
}
