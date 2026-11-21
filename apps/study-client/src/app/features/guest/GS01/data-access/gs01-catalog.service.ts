import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type {
  GuestCategoryPage,
  GuestPublicCoursePage,
} from '../../shared/models/guest-course.models';

export interface GS01CatalogQuery {
  page: number;
  sort?: string;
}

@Injectable({ providedIn: 'root' })
export class GS01CatalogService {
  private readonly api = inject(StudyApiService);

  getCategories(): Observable<ApiEnvelope<GuestCategoryPage>> {
    return this.api.request<GuestCategoryPage>(STUDY_SERVER_APIS.API_005);
  }

  getCourses(query: GS01CatalogQuery): Observable<ApiEnvelope<GuestPublicCoursePage>> {
    let params = new HttpParams().set('page', query.page).set('size', 20);
    if (query.sort) params = params.set('sort', query.sort);

    return this.api.request<GuestPublicCoursePage>(STUDY_SERVER_APIS.API_006, { params });
  }
}
