import { Injectable, inject } from '@angular/core';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentLesson } from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST11LessonService {
  private readonly api = inject(StudentApiService);
  lesson(lessonId: string) {
    return this.api.request<StudentLesson>(STUDY_SERVER_APIS.API_024, {
      pathParams: { lesson_id: lessonId },
    });
  }
}
