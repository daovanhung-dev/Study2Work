import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type { GS02CourseSearchPage } from '../models/gs02-search.models';

@Injectable({ providedIn: 'root' })
export class GS02SearchService {
  private readonly api = inject(StudyApiService);

  search(query: string, page: number): Observable<ApiEnvelope<GS02CourseSearchPage>> {
    const params = new HttpParams().set('q', query).set('page', page);
    return this.api.request<GS02CourseSearchPage>(STUDY_SERVER_APIS.API_007, { params });
  }
}
