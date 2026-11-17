import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorLecture } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME05LectureDetailService {
  private readonly api = inject(MentorApiService);
  detail(lectureId: string) {
    return this.api.request<MentorLecture>(STUDY_SERVER_APIS.API_048, { pathParams: { lecture_id: lectureId } });
  }
}
