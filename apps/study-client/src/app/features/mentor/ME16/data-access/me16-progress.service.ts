import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { type ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import { type MentorStudentProgressPageDto } from '../models/me16-progress.models';

@Injectable({ providedIn: 'root' })
export class Me16ProgressService {
  private readonly api = inject(StudyApiService);

  /**
   * API #65 — GET /api/v1/mentor/courses/{course_id}/progress
   * Trả về toàn bộ roster đang hoạt động trong 1 trang (MentorStudentProgressPage).
   */
  getCourseProgress(courseId: number): Observable<ApiEnvelope<MentorStudentProgressPageDto>> {
    return this.api.request<MentorStudentProgressPageDto>(`mentor/courses/${courseId}/progress`, {
      method: 'GET',
    });
  }
}
