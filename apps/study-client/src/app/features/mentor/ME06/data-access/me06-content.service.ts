import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type { ContentNodeDto } from '../models/me06-content.models';

@Injectable({ providedIn: 'root' })
export class Me06ContentService {
  private readonly api = inject(StudyApiService);

  /**
   * API #49: GET /api/v1/mentor/courses/{course_id}/content
   * Giữ nguyên raw ApiEnvelope<ContentNodeDto[]> tại ranh giới data-access.
   */
  getCourseContents(courseId: number): Observable<ApiEnvelope<ContentNodeDto[]>> {
    return this.api.request<ContentNodeDto[]>(`mentor/courses/${courseId}/content`, {
      method: 'GET',
    });
  }
}
