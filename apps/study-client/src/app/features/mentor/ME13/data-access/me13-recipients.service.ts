import { inject, Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
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
      .request<MentorCourseItemDto[] | { items?: MentorCourseItemDto[] }>(
        STUDY_SERVER_APIS.API_046,
      )
      .pipe(
        map((envelope) => {
          const data = envelope.data;
          if (Array.isArray(data)) {
            return data;
          }
          return Array.isArray(data?.items) ? data.items : [];
        }),
      );
  }

  /**
   * API #62: GET /api/v1/mentor/courses/{course_id}/students
   */
  getCourseStudents(courseId: number): Observable<StudentSummaryDto[]> {
    return this.api
      .request<StudentSummaryDto[]>(STUDY_SERVER_APIS.API_062, {
        pathParams: { course_id: courseId },
      })
      .pipe(map((envelope) => envelope.data ?? []));
  }
}
