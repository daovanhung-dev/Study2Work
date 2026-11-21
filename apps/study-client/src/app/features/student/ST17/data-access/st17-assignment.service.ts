import { Injectable, inject } from '@angular/core';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentAssignment } from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST17AssignmentService {
  private readonly api = inject(StudentApiService);
  assignment(assignmentId: string) {
    return this.api.request<StudentAssignment>(STUDY_SERVER_APIS.API_033, {
      pathParams: { assignment_id: assignmentId },
    });
  }
}
