import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type { GuestCourseCurriculumPage } from '../models/gs03-curriculum.models';

@Injectable({ providedIn: 'root' })
export class GS03CurriculumService {
  private readonly api = inject(StudyApiService);

  getCourseCurriculum(courseId: string): Observable<ApiEnvelope<GuestCourseCurriculumPage>> {
    return this.api.request<GuestCourseCurriculumPage>(STUDY_SERVER_APIS.API_009, {
      pathParams: { course_id: courseId },
    });
  }
}
