import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentCourseSummary, StudentPage } from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST08CoursesService {
  private readonly api = inject(StudentApiService);

  courses(page: number, status?: 'ACTIVE' | 'COMPLETED') {
    let params = new HttpParams().set('page', page);
    if (status) params = params.set('status', status);
    return this.api.request<StudentPage<StudentCourseSummary>>(STUDY_SERVER_APIS.API_020, {
      params,
    });
  }
}
