import { HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type { GS05CourseReviewsPage } from '../models/gs05-reviews.models';

@Injectable({ providedIn: 'root' })
export class GS05ReviewsService {
  private readonly api = inject(StudyApiService);

  getCourseReviews(courseId: string, page: number): Observable<ApiEnvelope<GS05CourseReviewsPage>> {
    return this.api.request<GS05CourseReviewsPage>(STUDY_SERVER_APIS.API_010, {
      pathParams: { course_id: courseId },
      params: new HttpParams().set('page', page),
    });
  }
}
