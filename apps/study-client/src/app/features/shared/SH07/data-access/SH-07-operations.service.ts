import { Injectable, inject } from '@angular/core';
import { map } from 'rxjs';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type { OperationDto } from '../models/SH-07-operations.models';

@Injectable({ providedIn: 'root' })
export class SystemOperationsService {
  private readonly api = inject(StudyApiService);

  getOperation(id: string) {
    return this.api.request<OperationDto>(STUDY_SERVER_APIS.API_018, {
      pathParams: { operation_id: id },
    }).pipe(map((response) => {
      const operation = response?.data;
      if (
        response?.success !== true ||
        response.businessCode !== 'DESIGN_OPERATION_RETRIEVED' ||
        !operation ||
        typeof operation.id !== 'string' ||
        operation.id.toLowerCase() !== id.toLowerCase() ||
        operation.kind !== 'NOTIFICATION_DISPATCH' ||
        !['QUEUED', 'FAILED', 'SENT'].includes(operation.status) ||
        !Number.isSafeInteger(operation.owner_id) ||
        typeof operation.submitted_at !== 'string' ||
        typeof operation.updated_at !== 'string'
      ) throw new Error('Invalid operation response');
      return operation;
    }));
  }
}
