import { Injectable, inject } from '@angular/core';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentLessonResources } from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST12ResourcesService {
  private readonly api = inject(StudentApiService);
  resources(lessonId: string) {
    return this.api.request<StudentLessonResources>(STUDY_SERVER_APIS.API_026, {
      pathParams: { lesson_id: lessonId },
    });
  }
}
