import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
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
    return this.api.request<Me08ContentNodeDto[]>(STUDY_SERVER_APIS.API_049, {
      pathParams: { course_id: courseId },
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
    return this.api.request<Me08ContentNodeDto>(STUDY_SERVER_APIS.API_052, {
      pathParams: { content_id: contentId },
      body,
    });
  }

  /**
   * API #53: DELETE /api/v1/mentor/content/{content_id}
   * Soft-delete một Content chưa xuất bản và không còn mục con hoạt động.
   */
  deleteContent(contentId: number): Observable<ApiEnvelope<DeleteResultDto>> {
    return this.api.request<DeleteResultDto>(STUDY_SERVER_APIS.API_053, {
      pathParams: { content_id: contentId },
    });
  }
}
