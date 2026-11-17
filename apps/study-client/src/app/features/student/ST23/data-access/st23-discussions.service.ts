import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentDiscussion, StudentPage } from '../../shared/models/student-api.models';

@Injectable({ providedIn: 'root' })
export class ST23DiscussionsService {
  private readonly api = inject(StudentApiService);
  discussions(courseId: number | null, page: number) {
    let params = new HttpParams().set('page', page);
    if (courseId !== null) params = params.set('course_id', courseId);
    return this.api.request<StudentPage<StudentDiscussion>>(STUDY_SERVER_APIS.API_039, { params });
  }
}
