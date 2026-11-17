import { map } from 'rxjs';
import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { StudyApiService } from '../../../../core/http/study-api.service';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { Category, Course, Page } from '../models/SH-01-landing.models';

function record(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}
const nullableText = (value: unknown): value is string | null =>
  value === null || typeof value === 'string';
export function isCategory(value: unknown): value is Category {
  return (
    record(value) &&
    Number.isSafeInteger(value['id']) &&
    typeof value['name'] === 'string' &&
    typeof value['slug'] === 'string' &&
    nullableText(value['description'])
  );
}
export function isCourse(value: unknown): value is Course {
  if (!record(value) || !record(value['mentor'])) return false;
  const mentor = value['mentor'];
  return (
    Number.isSafeInteger(value['id']) &&
    typeof value['title'] === 'string' &&
    nullableText(value['description']) &&
    nullableText(value['thumbnail_url']) &&
    typeof value['price'] === 'string' &&
    typeof value['status'] === 'string' &&
    Number.isSafeInteger(mentor['id']) &&
    typeof mentor['full_name'] === 'string' &&
    nullableText(mentor['avatar_url'])
  );
}
export function readItems<T>(value: unknown, accepts: (item: unknown) => item is T): T[] {
  if (
    !record(value) ||
    value['success'] !== true ||
    value['businessCode'] !== 'DESIGN_RESOURCE_RETRIEVED' ||
    !record(value['data']) ||
    !Array.isArray(value['data']['items']) ||
    !value['data']['items'].every(accepts)
  ) {
    throw new Error('Invalid Study catalog response');
  }
  return value['data']['items'];
}

@Injectable({ providedIn: 'root' })
export class LandingApi {
  private readonly api = inject(StudyApiService);

  getCategories() {
    return this.api
      .request<Page<Category>>(STUDY_SERVER_APIS.API_005)
      .pipe(map((response) => readItems(response, isCategory)));
  }

  getCourses() {
    return this.api
      .request<Page<Course>>(STUDY_SERVER_APIS.API_006, {
        params: new HttpParams().set('page', '1').set('size', '6'),
      })
      .pipe(map((response) => readItems(response, isCourse)));
  }
}
