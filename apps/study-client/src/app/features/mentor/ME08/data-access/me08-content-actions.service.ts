import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorContent } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME08ContentActionsService {
  private readonly api = inject(MentorApiService);
  content(courseId: string) {
    return this.api.request<MentorContent[]>(STUDY_SERVER_APIS.API_049, { pathParams: { course_id: courseId } });
  }
  publish(contentId: string, published: boolean) {
    return this.api.request<MentorContent>(STUDY_SERVER_APIS.API_052, {
      pathParams: { content_id: contentId }, body: { published },
    });
  }
  delete(contentId: string) {
    return this.api.request<{ id: number; status: 'deleted'; deleted_at: string }>(STUDY_SERVER_APIS.API_053, {
      pathParams: { content_id: contentId },
    });
  }
}
