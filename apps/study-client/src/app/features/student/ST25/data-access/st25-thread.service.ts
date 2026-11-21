import { Injectable, inject } from '@angular/core';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentDiscussion, StudentPage } from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST25ThreadService {
  private readonly api = inject(StudentApiService);
  thread(discussionId: string) {
    return this.api.request<StudentPage<StudentDiscussion>>(STUDY_SERVER_APIS.API_042, {
      pathParams: { discussion_id: discussionId },
    });
  }
  reply(discussionId: string, content: string) {
    return this.api.request<StudentPage<StudentDiscussion>>(STUDY_SERVER_APIS.API_041, {
      pathParams: { discussion_id: discussionId },
      body: { content },
    });
  }
}
