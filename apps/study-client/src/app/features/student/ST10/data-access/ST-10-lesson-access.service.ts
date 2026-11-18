import { HttpContext } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { map } from 'rxjs';

import { HANDLE_FORBIDDEN_LOCALLY } from '../../../../core/auth/auth.interceptor';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type { VerifiedLessonAccess } from '../models/ST-10-lesson-access.models';

@Injectable({ providedIn: 'root' })
export class StudentLessonAccessService {
  private readonly api = inject(StudyApiService);

  checkAccess(lessonId: string) {
    return this.api.request<unknown>(STUDY_SERVER_APIS.API_022, {
      pathParams: { lesson_id: lessonId },
      context: new HttpContext().set(HANDLE_FORBIDDEN_LOCALLY, true),
    }).pipe(map((response) => readAccess(response, lessonId)));
  }
}

function readAccess(response: ApiEnvelope<unknown>, lessonId: string): VerifiedLessonAccess {
  const data = response.data;
  if (!response.success || response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isRecord(data) || !Number.isSafeInteger(data['id']) || String(data['id']) !== lessonId ||
      !Number.isSafeInteger(data['course_id']) || (data['course_id'] as number) < 1 ||
      typeof data['title'] !== 'string' || !data['title'].trim() || data['status'] !== 'PUBLISHED') {
    throw new Error('Phản hồi kiểm tra quyền bài học không hợp lệ.');
  }
  // #22 currently includes content/video_url. Neither field may enter screen state.
  return { lessonId: data['id'] as number, courseId: data['course_id'] as number, title: data['title'] };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}
