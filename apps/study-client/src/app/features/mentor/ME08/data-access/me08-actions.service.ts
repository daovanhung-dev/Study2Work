import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type {
  DeleteResultDto,
  Me08ContentNodeDto,
  PublishContentRequestDto,
} from '../models/me08-actions.models';

@Injectable({ providedIn: 'root' })
export class Me08ActionsService {
  private readonly api = inject(StudyApiService);

  /**
   * API #49: GET /api/v1/mentor/courses/{course_id}/content
   * Dùng để nạp thông tin node mục tiêu, đếm mục con trực tiếp và refresh sau mutation.
   */
  getCourseContents(courseId: number): Observable<ApiEnvelope<Me08ContentNodeDto[]>> {
    return this.api.request<Me08ContentNodeDto[]>(`mentor/courses/${courseId}/content`, {
      method: 'GET',
    });
  }

  /**
   * API #52: PATCH /api/v1/mentor/content/{content_id}/publish
   * Chuyển trạng thái APPROVED <-> PUBLISHED.
   */
  setPublishState(
    contentId: number,
    body: PublishContentRequestDto,
  ): Observable<ApiEnvelope<Me08ContentNodeDto>> {
    return this.api.request<Me08ContentNodeDto>(`mentor/content/${contentId}/publish`, {
      method: 'PATCH',
      body,
    });
  }

  /**
   * API #53: DELETE /api/v1/mentor/content/{content_id}
   * Soft-delete một Content chưa xuất bản và không còn mục con hoạt động.
   */
  deleteContent(contentId: number): Observable<ApiEnvelope<DeleteResultDto>> {
    return this.api.request<DeleteResultDto>(`mentor/content/${contentId}`, {
      method: 'DELETE',
    });
  }
}
