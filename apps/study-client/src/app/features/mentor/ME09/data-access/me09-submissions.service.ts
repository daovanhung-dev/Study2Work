import { Injectable, inject } from '@angular/core';
import { HttpParams } from '@angular/common/http';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorPage, MentorSubmission } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME09SubmissionsService {
  private readonly api = inject(MentorApiService);
  list(page: number, courseId: string, status: string) {
    let params = new HttpParams().set('page', page).set('size', 20);
    if (courseId) params = params.set('course_id', courseId);
    if (status) params = params.set('status', status);
    return this.api.request<MentorPage<MentorSubmission>>(STUDY_SERVER_APIS.API_054, { params });
  }
}
