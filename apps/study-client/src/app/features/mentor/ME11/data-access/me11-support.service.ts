import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { type ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import {
  type Me11CoursePageDto,
  type Me11QueryParams,
  type SupportRequestItemDto,
} from '../models/me11-support.models';

@Injectable({ providedIn: 'root' })
export class Me11SupportService {
  private readonly api = inject(StudyApiService);

  /**
   * API #46 — GET /api/v1/mentor/courses
   */
  getMentorCourses(page = 1, size = 50): Observable<ApiEnvelope<Me11CoursePageDto>> {
    const params = new HttpParams().set('page', String(page)).set('size', String(size));
    return this.api.request<Me11CoursePageDto>('mentor/courses', {
      method: 'GET',
      params,
    });
  }

  /**
   * API #58 — GET /api/v1/mentor/support/requests
   * Query hợp lệ: course_id?: int64, status?: string
   */
  getSupportRequests(
    query: Me11QueryParams = {},
  ): Observable<ApiEnvelope<SupportRequestItemDto[]>> {
    let params = new HttpParams();

    if (query.course_id !== undefined && query.course_id !== null) {
      params = params.set('course_id', String(query.course_id));
    }

    if (query.status && query.status.trim().length > 0) {
      params = params.set('status', query.status.trim());
    }

    return this.api.request<SupportRequestItemDto[]>('mentor/support/requests', {
      method: 'GET',
      params,
    });
  }
}
