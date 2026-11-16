import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminQuizStatistics } from '../../admin-api.models';

@Injectable({ providedIn: 'root' })
export class AD17ApiService {
  private readonly api = inject(AdminApiService);

  getStatistics(quizId: string) {
    return this.api.get<AdminQuizStatistics>(STUDY_SERVER_APIS.API_091, {
      pathParams: { quiz_id: quizId },
    });
  }
}
