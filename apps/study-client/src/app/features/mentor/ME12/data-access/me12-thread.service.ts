import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { type ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import {
  type ReplySupportRequestDto,
  type SupportRequestDetailDto,
} from '../models/me12-thread.models';

@Injectable({ providedIn: 'root' })
export class Me12ThreadService {
  private readonly api = inject(StudyApiService);

  /**
   * API #59 — GET /api/v1/mentor/support/{request_id}
   */
  getSupportRequestDetail(requestId: number): Observable<ApiEnvelope<SupportRequestDetailDto>> {
    return this.api.request<SupportRequestDetailDto>(`mentor/support/${requestId}`, {
      method: 'GET',
    });
  }

  /**
   * API #60 — POST /api/v1/mentor/support/{request_id}/reply
   */
  sendReply(
    requestId: number,
    payload: ReplySupportRequestDto,
  ): Observable<ApiEnvelope<SupportRequestDetailDto>> {
    return this.api.request<SupportRequestDetailDto>(`mentor/support/${requestId}/reply`, {
      method: 'POST',
      body: payload,
    });
  }

  /**
   * API #61 — PATCH /api/v1/mentor/support/{request_id}/resolve
   */
  resolveRequest(requestId: number): Observable<ApiEnvelope<SupportRequestDetailDto>> {
    return this.api.request<SupportRequestDetailDto>(`mentor/support/${requestId}/resolve`, {
      method: 'PATCH',
    });
  }
}
