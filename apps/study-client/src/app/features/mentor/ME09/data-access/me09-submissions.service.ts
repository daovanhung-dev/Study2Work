import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { type ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import {
  type Me09QueryParams,
  type MentorCoursePageDto,
  type SubmissionPageDto,
} from '../models/me09-submissions.models';

@Injectable({ providedIn: 'root' })
export class Me09SubmissionsService {
  private readonly api = inject(StudyApiService);

  /**
   * API #46 — GET /api/v1/mentor/courses
   * Lấy danh sách khóa học do Mentor trực tiếp phụ trách để nạp vào bộ lọc khóa học.
   */
  getMentorCourses(page = 1, size = 50): Observable<ApiEnvelope<MentorCoursePageDto>> {
    const params = new HttpParams().set('page', String(page)).set('size', String(size));
    return this.api.request<MentorCoursePageDto>('mentor/courses', {
      method: 'GET',
      params,
    });
  }

  /**
   * API #54 — GET /api/v1/mentor/submissions
   * Query hợp lệ: course_id?: int64, status?: string, page?: int32 (mặc định 1).
   * Không gửi q, size hoặc sort vì Study Server dùng ConfigDict(extra="forbid").
   */
  getSubmissions(query: Me09QueryParams): Observable<ApiEnvelope<SubmissionPageDto>> {
    let params = new HttpParams().set('page', String(query.page ?? 1));

    if (query.course_id !== undefined && query.course_id !== null) {
      params = params.set('course_id', String(query.course_id));
    }

    if (query.status && query.status.trim().length > 0) {
      params = params.set('status', query.status.trim());
    }

    return this.api.request<SubmissionPageDto>('mentor/submissions', {
      method: 'GET',
      params,
    });
  }
}
