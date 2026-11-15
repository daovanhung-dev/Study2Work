import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminContent } from '../../admin-api.models';

@Injectable({ providedIn: 'root' })
export class AD11ApiService {
  private readonly api = inject(AdminApiService);

  getContent(contentId: string) {
    return this.api.get<AdminContent>(STUDY_SERVER_APIS.API_079, {
      pathParams: { content_id: contentId },
    });
  }
}
