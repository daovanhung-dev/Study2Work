import { Injectable, inject } from '@angular/core';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type {
  StudentAssignment,
  StudentSubmission,
  StudentUploadAsset,
} from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST18SubmissionService {
  private readonly api = inject(StudentApiService);
  assignment(assignmentId: string) {
    return this.api.request<StudentAssignment>(STUDY_SERVER_APIS.API_033, {
      pathParams: { assignment_id: assignmentId },
    });
  }
  upload(file: File, courseId: number) {
    const body = new FormData();
    body.append('file', file);
    body.append('purpose', 'SUBMISSION');
    body.append('course_id', String(courseId));
    return this.api.request<StudentUploadAsset>(STUDY_SERVER_APIS.API_034, { body });
  }
  submit(assignmentId: string, content: string | null, uploadId: number | null) {
    return this.api.request<StudentSubmission>(STUDY_SERVER_APIS.API_035, {
      pathParams: { assignment_id: assignmentId },
      body: { content, upload_id: uploadId },
    });
  }
}
