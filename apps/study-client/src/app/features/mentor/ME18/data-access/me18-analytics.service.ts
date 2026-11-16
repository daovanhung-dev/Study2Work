import { inject, Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudyApiService } from '../../../../core/http/study-api.service';
import { MentorCourseActivityAnalyticsDto } from '../models/me18-analytics.models';

@Injectable({ providedIn: 'root' })
export class Me18AnalyticsService {
  private readonly api = inject(StudyApiService);

  /**
   * API #66: GET /api/v1/mentor/courses/{course_id}/analytics
   * Backend does not accept period/from/to query params; returns 3 proxy metrics.
   */
  getCourseAnalytics(courseId: number): Observable<MentorCourseActivityAnalyticsDto> {
    return this.api
      .request<MentorCourseActivityAnalyticsDto>(STUDY_SERVER_APIS.API_066, {
        pathParams: { course_id: courseId },
      })
      .pipe(map((envelope) => envelope.data));
  }
}
