import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { map } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type { CoursePage, EnrolledCourse } from '../models/ST-08-courses.models';

@Injectable({ providedIn: 'root' })
export class StudentCoursesService {
  private readonly api = inject(StudyApiService);

  getCourses(page: number) {
    return this.api.request<unknown>(STUDY_SERVER_APIS.API_020, {
      params: new HttpParams().set('page', page),
    }).pipe(map(readCoursesPage));
  }
}

export function readCoursesPage(response: ApiEnvelope<unknown>): CoursePage {
  const data = response.data;
  if (!response.success || response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' || !isRecord(data) ||
      !Array.isArray(data['items']) || !isRecord(data['pagination'])) {
    throw new Error('Phản hồi danh sách khóa học từ API #20 không hợp lệ.');
  }

  const pagination = data['pagination'];
  const page = pagination['page'];
  const size = pagination['size'];
  const total = pagination['total'];
  const totalPages = pagination['total_pages'];
  if (!Number.isInteger(page) || !Number.isInteger(size) || !Number.isInteger(total) ||
      !Number.isInteger(totalPages) || (page as number) < 1 || (size as number) < 1 ||
      (total as number) < 0 || (totalPages as number) < 0) {
    throw new Error('Phân trang khóa học từ API #20 không hợp lệ.');
  }

  const items: EnrolledCourse[] = data['items'].map((item: unknown) => {
    if (!isRecord(item) || !Number.isSafeInteger(item['course_id']) ||
        (item['course_id'] as number) < 1 || typeof item['name'] !== 'string' ||
        typeof item['enrollment_status'] !== 'string' || typeof item['enrolled_at'] !== 'string') {
      throw new Error('Dữ liệu khóa học từ API #20 không hợp lệ.');
    }
    return {
      course_id: item['course_id'] as number,
      name: item['name'],
      description: typeof item['description'] === 'string' ? item['description'] : null,
      thumbnail_url: typeof item['thumbnail_url'] === 'string' ? item['thumbnail_url'] : null,
      enrollment_status: item['enrollment_status'],
      enrolled_at: item['enrolled_at'],
    };
  });

  return {
    items,
    pagination: { page: page as number, size: size as number, total: total as number, total_pages: totalPages as number },
  };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}
