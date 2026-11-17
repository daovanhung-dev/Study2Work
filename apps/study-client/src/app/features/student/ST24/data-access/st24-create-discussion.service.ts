import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type {
  StudentCourseSummary,
  StudentDiscussion,
  StudentPage,
} from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST24CreateDiscussionService {
  private readonly api = inject(StudentApiService);
  courses() {
    return this.api.request<StudentPage<StudentCourseSummary>>(STUDY_SERVER_APIS.API_020);
  }
  create(courseId: number, title: string, content: string) {
    return this.api.request<StudentDiscussion>(STUDY_SERVER_APIS.API_040, {
      body: { course_id: courseId, title, content },
    });
  }
  refresh(courseId: number) {
    return this.api.request<StudentPage<StudentDiscussion>>(STUDY_SERVER_APIS.API_039, {
      params: new HttpParams().set('course_id', courseId).set('page', 1),
    });
  }
}
