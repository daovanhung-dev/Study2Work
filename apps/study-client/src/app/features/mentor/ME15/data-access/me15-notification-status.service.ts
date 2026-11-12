import { inject, Injectable } from '@angular/core';
import { forkJoin, map, Observable, of } from 'rxjs';
import { StudyApiService } from '../../../../core/http/study-api.service';
import {
  NotificationStatusItemVm,
  NotificationStatusOperationDto,
} from '../models/me15-notification-status.models';

@Injectable({ providedIn: 'root' })
export class Me15NotificationStatusService {
  private readonly api = inject(StudyApiService);

  /**
   * API #64: GET /api/v1/mentor/notifications/:notificationId/status
   */
  getNotificationStatus(notificationId: number): Observable<NotificationStatusOperationDto> {
    return this.api
      .request<NotificationStatusOperationDto>(`mentor/notifications/${notificationId}/status`, {
        method: 'GET',
      })
      .pipe(map((envelope) => envelope.data));
  }

  getBatchStatuses(notificationIds: readonly number[]): Observable<NotificationStatusItemVm[]> {
    if (notificationIds.length === 0) {
      return of([]);
    }
    return forkJoin(
      notificationIds.map((id) =>
        this.getNotificationStatus(id).pipe(
          map((res) => ({
            notificationId: id,
            operationId: res.operation_id,
            status: res.status,
          })),
        ),
      ),
    );
  }
}
