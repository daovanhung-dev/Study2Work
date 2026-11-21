import { Injectable, inject } from '@angular/core';
import { map } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminDiscussion, AdminPage } from '../../admin-api.models';
import { isAD23DiscussionEnvelope } from '../models/ad23-discussion.models';

@Injectable({ providedIn: 'root' })
export class AD23ApiService {
  private readonly api = inject(AdminApiService);

  getDiscussion(discussionId: string) {
    return this.api
      .get<AdminPage<AdminDiscussion>>(STUDY_SERVER_APIS.API_098, {
        pathParams: { discussion_id: discussionId },
      })
      .pipe(
        map((response) => {
          const candidate: unknown = response;
          if (!isAD23DiscussionEnvelope(candidate, discussionId)) {
            throw new Error('API #98 returned a discussion that does not match the route.');
          }
          return response;
        }),
      );
  }
}
