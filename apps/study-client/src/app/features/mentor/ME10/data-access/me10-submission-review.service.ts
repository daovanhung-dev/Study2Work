import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type { MentorSubmission } from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME10SubmissionReviewService {
  private readonly api = inject(MentorApiService);
  detail(submissionId: string) {
    return this.api.request<MentorSubmission>(STUDY_SERVER_APIS.API_055, { pathParams: { submission_id: submissionId } });
  }
  grade(submissionId: string, score: number, rubricItems: string) {
    return this.api.request<MentorSubmission>(STUDY_SERVER_APIS.API_056, {
      pathParams: { submission_id: submissionId }, body: { score, rubric_items: rubricItems },
    });
  }
  feedback(submissionId: string, feedbackText: string, attachments: string) {
    return this.api.request<MentorSubmission>(STUDY_SERVER_APIS.API_057, {
      pathParams: { submission_id: submissionId }, body: { feedback_text: feedbackText, attachments },
    });
  }
}
