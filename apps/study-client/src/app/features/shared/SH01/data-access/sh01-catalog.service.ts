import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type { SH01CategoryPage, SH01PublicCoursePage } from '../models/sh01-catalog.models';

@Injectable({ providedIn: 'root' })
export class SH01CatalogService {
  private readonly api = inject(StudyApiService);

  getCategories(): Observable<ApiEnvelope<SH01CategoryPage>> {
    return this.api.request<SH01CategoryPage>(STUDY_SERVER_APIS.API_005);
  }

  getPublishedCourses(): Observable<ApiEnvelope<SH01PublicCoursePage>> {
    const params = new HttpParams().set('page', 1).set('size', 6);
    return this.api.request<SH01PublicCoursePage>(STUDY_SERVER_APIS.API_006, { params });
  }
}
