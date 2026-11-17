import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorSupportRequest } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME12SupportThreadService {
  private readonly api = inject(MentorApiService);
  detail(requestId: string) {
    return this.api.request<MentorSupportRequest>(STUDY_SERVER_APIS.API_059, { pathParams: { request_id: requestId } });
  }
  reply(requestId: string, message: string, attachmentRefs = '[]') {
    return this.api.request<MentorSupportRequest>(STUDY_SERVER_APIS.API_060, {
      pathParams: { request_id: requestId }, body: { message, attachment_refs: attachmentRefs },
    });
  }
  resolve(requestId: string) {
    return this.api.request<MentorSupportRequest>(STUDY_SERVER_APIS.API_061, {
      pathParams: { request_id: requestId },
    });
  }
}
