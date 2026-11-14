import type { St04CoursePage, St04CourseSummary } from '../models/ST-04-enroll-course.models';
import { map } from 'rxjs';
import { Injectable, inject } from '@angular/core';

import { StudyApiService } from '../../../../core/http/study-api.service';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';

export function getSt04Course(response: {
  success: boolean;
  businessCode: string;
  data: St04CoursePage | null;
}): St04CourseSummary | null {
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
export class St04CourseApi {
  private readonly api = inject(StudyApiService);

  getCourse(rawCourseId: string) {
    return this.api
      .request<St04CoursePage>(STUDY_SERVER_APIS.API_008, {
        pathParams: { course_id: rawCourseId },
      })
      .pipe(map(getSt04Course));
  }
}
