import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorContent } from '../../shared/models/mentor-api.models';

export interface MentorContentDraft { course_id?: number; content_type: string; title: string; payload: Record<string, unknown> }

@Injectable({ providedIn: 'root' })
export class ME07ContentEditorService {
  private readonly api = inject(MentorApiService);
  list(courseId: string) {
    return this.api.request<MentorContent[]>(STUDY_SERVER_APIS.API_049, { pathParams: { course_id: courseId } });
  }
  create(body: MentorContentDraft) {
    return this.api.request<MentorContent>(STUDY_SERVER_APIS.API_050, { body });
  }
  update(contentId: string, body: Omit<MentorContentDraft, 'course_id'>) {
    return this.api.request<MentorContent>(STUDY_SERVER_APIS.API_051, { pathParams: { content_id: contentId }, body });
  }
}
