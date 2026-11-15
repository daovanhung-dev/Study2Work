import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminDiscussion, AdminPage } from '../../admin-api.models';

@Injectable({ providedIn: 'root' })
export class AD23ApiService {
  private readonly api = inject(AdminApiService);

  getDiscussion(discussionId: string) {
    return this.api.get<AdminPage<AdminDiscussion>>(STUDY_SERVER_APIS.API_098, {
      pathParams: { discussion_id: discussionId },
    });
  }
}
