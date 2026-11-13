import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { type ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import { type StudentCourseProgressDto } from '../models/me17-student-progress.models';

@Injectable({ providedIn: 'root' })
export class Me17StudentProgressService {
  private readonly api = inject(StudyApiService);

  /**
   * API #67 — GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress
   */
  getStudentCourseProgress(
    courseId: number,
    studentId: number,
  ): Observable<ApiEnvelope<StudentCourseProgressDto>> {
    return this.api.request<StudentCourseProgressDto>(
      `mentor/courses/${courseId}/students/${studentId}/progress`,
      {
        method: 'GET',
      },
    );
  }
}
