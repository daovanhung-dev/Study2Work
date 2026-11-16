import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { type ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import {
  type FeedbackSubmissionRequestDto,
  type GradeSubmissionRequestDto,
  type SubmissionDetailDto,
} from '../models/me10-grading.models';

@Injectable({ providedIn: 'root' })
export class Me10GradingService {
  private readonly api = inject(StudyApiService);

  /**
   * API #55 — GET /api/v1/mentor/submissions/{submission_id}
   */
  getSubmissionDetail(submissionId: number): Observable<ApiEnvelope<SubmissionDetailDto>> {
    return this.api.request<SubmissionDetailDto>(STUDY_SERVER_APIS.API_055, {
      pathParams: { submission_id: submissionId },
    });
  }

  /**
   * API #56 — POST /api/v1/mentor/submissions/{submission_id}/grade
   */
  saveGrade(
    submissionId: number,
    payload: GradeSubmissionRequestDto,
  ): Observable<ApiEnvelope<SubmissionDetailDto>> {
    return this.api.request<SubmissionDetailDto>(STUDY_SERVER_APIS.API_056, {
      pathParams: { submission_id: submissionId },
      body: payload,
    });
  }

  /**
   * API #57 — POST /api/v1/mentor/submissions/{submission_id}/feedback
   */
  saveFeedback(
    submissionId: number,
    payload: FeedbackSubmissionRequestDto,
  ): Observable<ApiEnvelope<SubmissionDetailDto>> {
    return this.api.request<SubmissionDetailDto>(STUDY_SERVER_APIS.API_057, {
      pathParams: { submission_id: submissionId },
      body: payload,
    });
  }
}
