import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type {
  CreateContentRequestDto,
  Me07ContentNodeDto,
  UpdateContentRequestDto,
} from '../models/me07-editor.models';

@Injectable({ providedIn: 'root' })
export class Me07EditorService {
  private readonly api = inject(StudyApiService);

  /**
   * API #49: GET /api/v1/mentor/courses/{course_id}/content
   * Dùng để nạp node hiện hữu khi mở ME-07 ở chế độ chỉnh sửa.
   */
  getCourseContents(courseId: number): Observable<ApiEnvelope<Me07ContentNodeDto[]>> {
    return this.api.request<Me07ContentNodeDto[]>(`mentor/courses/${courseId}/content`, {
      method: 'GET',
    });
  }

  /**
   * API #50: POST /api/v1/mentor/content
   * Tạo node Content mới ở trạng thái PENDING_REVIEW.
   */
  createContent(body: CreateContentRequestDto): Observable<ApiEnvelope<Me07ContentNodeDto>> {
    return this.api.request<Me07ContentNodeDto>('mentor/content', {
      method: 'POST',
      body,
    });
  }

  /**
   * API #51: PUT /api/v1/mentor/content/{content_id}
   * Lưu snapshot phiên bản cũ và cập nhật Content về trạng thái PENDING_REVIEW.
   */
  updateContent(
    contentId: number,
    body: UpdateContentRequestDto,
  ): Observable<ApiEnvelope<Me07ContentNodeDto>> {
    return this.api.request<Me07ContentNodeDto>(`mentor/content/${contentId}`, {
      method: 'PUT',
      body,
    });
  }
}
