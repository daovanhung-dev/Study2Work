import { Injectable, inject } from '@angular/core';
import { HttpParams } from '@angular/common/http';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorSupportRequest } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME11SupportInboxService {
  private readonly api = inject(MentorApiService);
  list(courseId: string, status: string) {
    let params = new HttpParams();
    if (courseId) params = params.set('course_id', courseId);
    if (status) params = params.set('status', status);
    return this.api.request<MentorSupportRequest[]>(STUDY_SERVER_APIS.API_058, { params });
  }
}
