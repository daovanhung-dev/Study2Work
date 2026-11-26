import { Injectable, inject } from '@angular/core';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentLesson } from '../../shared/models/student-api.models';

export interface LessonProgressPayload {
  percent: number;
  completed: boolean;
}

@Injectable({ providedIn: 'root' })
export class ST11LessonService {
  private readonly api = inject(StudentApiService);

  lesson(lessonId: string) {
    return this.api.request<StudentLesson>(STUDY_SERVER_APIS.API_024, {
      pathParams: { lesson_id: lessonId },
    });
  }

  updateProgress(lessonId: string, body: LessonProgressPayload) {
    return this.api.request<StudentLesson>(STUDY_SERVER_APIS.API_025, {
      pathParams: { lesson_id: lessonId },
      body,
    });
  }

  nextLesson(lessonId: string) {
    return this.api.request<StudentLesson>(STUDY_SERVER_APIS.API_027, {
      pathParams: { lesson_id: lessonId },
    });
  }
}
