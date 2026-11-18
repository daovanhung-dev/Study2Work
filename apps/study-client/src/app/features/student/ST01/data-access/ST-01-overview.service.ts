import { Injectable, inject } from '@angular/core';
import { map } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type { Achievement, EnrolledCourse, StudentNotification } from '../models/ST-01-overview.models';

interface Page<T> {
  items: T[];
  pagination: { total: number };
}

@Injectable({ providedIn: 'root' })
export class StudentOverviewService {
  private readonly api = inject(StudyApiService);

  getCourses() {
    return this.api.request<Page<EnrolledCourse>>(STUDY_SERVER_APIS.API_020).pipe(map(readPage));
  }

  getProgressContract() {
    return this.api.request<unknown>(STUDY_SERVER_APIS.API_021).pipe(
      map((response) => {
        verifyEnvelope(response);
        const profile = response.data;
        if (!profile || typeof profile !== 'object' ||
            typeof (profile as Record<string, unknown>)['full_name'] !== 'string' ||
            typeof (profile as Record<string, unknown>)['id'] !== 'number') {
          throw new Error('API #21 trả dữ liệu khác contract hồ sơ hiện tại.');
        }
        // API #21 currently returns UserProfile, not aggregate/course progress.
        return 'API #21 đã phản hồi nhưng chỉ cung cấp hồ sơ, chưa có số liệu tiến độ.';
      }),
    );
  }

  getAchievements() {
    return this.api.request<Page<Achievement>>(STUDY_SERVER_APIS.API_038).pipe(map(readPage));
  }

  getNotifications() {
    return this.api.request<Page<StudentNotification>>(STUDY_SERVER_APIS.API_043).pipe(map(readPage));
  }
}

function verifyEnvelope(response: ApiEnvelope<unknown>): void {
  if (!response?.success || response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
    throw new Error('Phản hồi API không đúng contract.');
  }
}

function readPage<T>(response: ApiEnvelope<Page<T>>): { items: T[]; total: number } {
  verifyEnvelope(response);
  if (!response.data || !Array.isArray(response.data.items) ||
      !Number.isInteger(response.data.pagination?.total) || response.data.pagination.total < 0) {
    throw new Error('Danh sách từ API không đúng contract.');
  }
  return { items: response.data.items, total: response.data.pagination.total };
}
