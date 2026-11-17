import { Injectable, inject } from '@angular/core';
import { HttpParams } from '@angular/common/http';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorCourse, MentorPage } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME04LectureCreateService {
  private readonly api = inject(MentorApiService);
  courses() {
    return this.api.request<MentorPage<MentorCourse>>(STUDY_SERVER_APIS.API_046, {
      params: new HttpParams().set('page', 1).set('size', 100),
    });
  }
}
