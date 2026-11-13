import { inject, Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { StudyApiService } from '../../../../core/http/study-api.service';
import { MentorCourseItemDto, StudentSummaryDto } from '../models/me13-recipients.models';

@Injectable({ providedIn: 'root' })
export class Me13RecipientsService {
  private readonly api = inject(StudyApiService);

  /**
   * API #46: GET /api/v1/mentor/courses
   */
  getMentorCourses(): Observable<MentorCourseItemDto[]> {
    return this.api
      .request<MentorCourseItemDto[]>('mentor/courses', { method: 'GET' })
      .pipe(map((envelope) => envelope.data ?? []));
  }

  /**
   * API #62: GET /api/v1/mentor/courses/:courseId/students
   */
  getCourseStudents(courseId: number): Observable<StudentSummaryDto[]> {
    return this.api
      .request<StudentSummaryDto[]>(`mentor/courses/${courseId}/students`, { method: 'GET' })
      .pipe(map((envelope) => envelope.data ?? []));
  }
}
