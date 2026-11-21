import { Injectable, inject } from '@angular/core';
import { HttpParams } from '@angular/common/http';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorCourse, MentorPage } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME02CoursesService {
  private readonly api = inject(MentorApiService);
  list(page: number, status: string) {
    let params = new HttpParams().set('page', page).set('size', 20);
    if (status) params = params.set('status', status);
    return this.api.request<MentorPage<MentorCourse>>(STUDY_SERVER_APIS.API_046, { params });
  }
}
