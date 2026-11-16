import { inject, Injectable } from '@angular/core';
import { forkJoin, map, Observable, of } from 'rxjs';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudyApiService } from '../../../../core/http/study-api.service';
import {
  NotificationStatusItemVm,
  NotificationStatusOperationDto,
} from '../models/me15-notification-status.models';

@Injectable({ providedIn: 'root' })
export class Me15NotificationStatusService {
  private readonly api = inject(StudyApiService);

  /**
   * API #64: GET /api/v1/mentor/notifications/{notification_id}/status
   */
  getNotificationStatus(notificationId: number): Observable<NotificationStatusOperationDto> {
    return this.api
      .request<NotificationStatusOperationDto>(STUDY_SERVER_APIS.API_064, {
        pathParams: { notification_id: notificationId },
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
