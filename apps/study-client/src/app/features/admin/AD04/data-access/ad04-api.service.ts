import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminUserProfile } from '../../admin-api.models';

@Injectable({ providedIn: 'root' })
export class AD04ApiService {
  private readonly api = inject(AdminApiService);

  getUser(userId: string) {
    return this.api.get<AdminUserProfile>(STUDY_SERVER_APIS.API_069, {
      pathParams: { user_id: userId },
    });
  }
}
