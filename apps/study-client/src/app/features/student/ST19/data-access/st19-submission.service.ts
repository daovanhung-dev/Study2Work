import { Injectable, inject } from '@angular/core';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentSubmission } from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST19SubmissionService {
  private readonly api = inject(StudentApiService);
  submission(submissionId: string) {
    return this.api.request<StudentSubmission>(STUDY_SERVER_APIS.API_036, {
      pathParams: { submission_id: submissionId },
    });
  }
}
