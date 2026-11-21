import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminLesson } from '../../admin-api.models';
import { adminQueryParams } from '../../admin-query-params';

@Injectable({ providedIn: 'root' })
export class AD12ApiService {
  private readonly api = inject(AdminApiService);

  getLessons(query: { course?: string; status?: string } = {}) {
    return this.api.get<readonly AdminLesson[]>(STUDY_SERVER_APIS.API_082, {
      params: adminQueryParams(query),
    });
  }
}
