import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type { GS06Resource } from '../models/gs06-resource-screen-state.model';

@Injectable({ providedIn: 'root' })
export class GS06ResourcesService {
  private readonly api = inject(StudyApiService);

  resources(courseId: string) {
    return this.api.request<GS06Resource[]>(STUDY_SERVER_APIS.API_011, {
      pathParams: { course_id: courseId },
    });
  }
}
