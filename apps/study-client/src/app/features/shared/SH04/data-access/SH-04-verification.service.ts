import type { VerificationState } from '../models/SH-04-verification.models';
import { HttpErrorResponse } from '@angular/common/http';
import { catchError, map, of, type Observable } from 'rxjs';
import type { VerificationResult } from '../models/SH-04-verification.models';
import { Injectable, inject } from '@angular/core';

import { StudyApiService } from '../../../../core/http/study-api.service';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type {
  VerificationRequest,
  VerificationResponse,
} from '../models/SH-04-verification.models';

export function mapVerificationResponse(status: number, body: unknown): VerificationState {
  if (status !== 202 || typeof body !== 'object' || body === null) return 'unknown';
  const response = body as Record<string, unknown>;
  const data = response['data'];
  if (
    response['success'] !== true ||
    response['businessCode'] !== 'DESIGN_OPERATION_ACCEPTED' ||
    typeof data !== 'object' ||
    data === null ||
    !('status' in data) ||
    typeof data.status !== 'string'
  )
    return 'unknown';
  return data.status === 'accepted' ? 'accepted' : 'unmapped';
}
export function mapVerificationError(status: number, body: unknown): VerificationState {
  const code =
    typeof body === 'object' && body !== null && 'businessCode' in body ? body.businessCode : null;
  if (status === 422 && code === 'DESIGN_VALIDATION_ERROR') return 'invalid';
  if (status === 500 && code === 'DESIGN_INTERNAL_ERROR') return 'provider-error';
  return 'unknown';
}

@Injectable({ providedIn: 'root' })
export class VerificationApi {
  private readonly api = inject(StudyApiService);

  dispatch(request: VerificationRequest): Observable<VerificationResult> {
    return this.api
      .requestResponse<VerificationResponse>(STUDY_SERVER_APIS.API_002, {
        body: request,
      })
      .pipe(
        map((response) => ({
          state: mapVerificationResponse(response.status, response.body),
          httpStatus: response.status,
        })),
        catchError((error: unknown) =>
          of({
            state:
              error instanceof HttpErrorResponse
                ? mapVerificationError(error.status, error.error)
                : ('unknown' as const),
            httpStatus: error instanceof HttpErrorResponse ? error.status || null : null,
          }),
        ),
      );
  }
}
