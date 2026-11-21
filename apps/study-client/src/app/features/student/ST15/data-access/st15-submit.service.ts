import { Injectable, inject } from '@angular/core';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentQuizAttempt } from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST15SubmitService {
  private readonly api = inject(StudentApiService);
  submit(attemptId: string) {
    return this.api.request<StudentQuizAttempt>(STUDY_SERVER_APIS.API_031, {
      pathParams: { attempt_id: attemptId },
    });
  }
}
