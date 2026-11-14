import type { St05CoursePage, St05CourseSummary } from '../models/ST-05-checkout-course.models';
import { map } from 'rxjs';
import { Injectable, inject } from '@angular/core';

import { StudyApiService } from '../../../../core/http/study-api.service';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';

export function getSt05Course(response: {
  success: boolean;
  businessCode: string;
  data: St05CoursePage | null;
}): St05CourseSummary | null {
  const item = response.data?.items?.[0];
  return response.success &&
    response.businessCode === 'DESIGN_RESOURCE_RETRIEVED' &&
    Array.isArray(response.data?.items) &&
    response.data.items.length === 1 &&
    item &&
    Number.isSafeInteger(item.id) &&
    (item.description === null || typeof item.description === 'string') &&
    typeof item.status === 'string' &&
    typeof item.title === 'string' &&
    typeof item.price === 'string'
    ? item
    : null;
}

@Injectable({ providedIn: 'root' })
export class St05CourseApi {
  private readonly api = inject(StudyApiService);

  getCourse(rawCourseId: string) {
    return this.api
      .request<St05CoursePage>(STUDY_SERVER_APIS.API_008, {
        pathParams: { course_id: rawCourseId },
      })
      .pipe(map(getSt05Course));
  }
}
