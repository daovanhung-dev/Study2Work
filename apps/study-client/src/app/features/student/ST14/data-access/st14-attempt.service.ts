import { Injectable, inject } from '@angular/core';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentQuiz, StudentQuizAttempt } from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST14AttemptService {
  private readonly api = inject(StudentApiService);
  quiz(quizId: string) {
    return this.api.request<StudentQuiz>(STUDY_SERVER_APIS.API_028, {
      pathParams: { quiz_id: quizId },
    });
  }
  save(attemptId: string, questionId: number, choiceIds: number[] | null, answer: string) {
    return this.api.request<StudentQuizAttempt>(STUDY_SERVER_APIS.API_030, {
      pathParams: { attempt_id: attemptId },
      body: { question_id: questionId, choice_ids: choiceIds, answer },
    });
  }
}
