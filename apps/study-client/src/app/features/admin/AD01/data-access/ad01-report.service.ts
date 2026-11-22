import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { AD01DateRange } from '../models/ad01-report.model';

@Injectable({ providedIn: 'root' })
export class AD01ReportService {
  private readonly adminApi = inject(AdminApiService);

  /** Gửi hai ngày inclusive tới API #101 và giữ nguyên envelope trả về. */
  getSummary(range: AD01DateRange): Observable<ApiEnvelope<unknown>> {
    const params = new HttpParams().set('from', range.from).set('to', range.to);
    return this.adminApi.get<unknown>(STUDY_SERVER_APIS.API_101, { params });
  }
}
