import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

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
    return this.api.request<SubmissionDetailDto>(`mentor/submissions/${submissionId}`, {
      method: 'GET',
    });
  }

  /**
   * API #56 — POST /api/v1/mentor/submissions/{submission_id}/grade
   */
  saveGrade(
    submissionId: number,
    payload: GradeSubmissionRequestDto,
  ): Observable<ApiEnvelope<SubmissionDetailDto>> {
    return this.api.request<SubmissionDetailDto>(`mentor/submissions/${submissionId}/grade`, {
      method: 'POST',
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
    return this.api.request<SubmissionDetailDto>(`mentor/submissions/${submissionId}/feedback`, {
      method: 'POST',
      body: payload,
    });
  }
}
