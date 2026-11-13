import { inject, Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { StudyApiService } from '../../../../core/http/study-api.service';
import {
  CourseContentSummaryDto,
  CreateNotificationRequestDto,
  CreateNotificationResultDto,
  OperationResponseDto,
} from '../models/me14-create-notification.models';

@Injectable({ providedIn: 'root' })
export class Me14CreateNotificationService {
  private readonly api = inject(StudyApiService);

  /**
   * API #49: GET /api/v1/mentor/courses/:courseId/contents
   */
  getCourseContents(courseId: number): Observable<CourseContentSummaryDto[]> {
    return this.api
      .request<CourseContentSummaryDto[]>(`mentor/courses/${courseId}/contents`, {
        method: 'GET',
      })
      .pipe(map((envelope) => envelope.data ?? []));
  }

  /**
   * API #63: POST /api/v1/mentor/notifications -> 202 Accepted
   */
  createNotification(
    payload: CreateNotificationRequestDto,
  ): Observable<CreateNotificationResultDto> {
    return this.api
      .request<OperationResponseDto>('mentor/notifications', {
        method: 'POST',
        body: payload,
      })
      .pipe(
        map((envelope) => {
          const rawIds = (envelope.meta as { notification_ids?: unknown } | undefined)
            ?.notification_ids;
          const notificationIds = Array.isArray(rawIds)
            ? rawIds.filter((id): id is number => typeof id === 'number' && id > 0)
            : [];
          return {
            operation: envelope.data,
            notificationIds,
          };
        }),
      );
  }
}
