import { Injectable, inject } from '@angular/core';
import { HttpParams } from '@angular/common/http';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { MentorApiService } from '../../../../core/http/mentor-api.service';
import type {
  MentorCourse,
  MentorLecture,
  MentorPage,
  MentorUploadAsset,
} from '../../shared/models/mentor-api.models';

@Injectable({ providedIn: 'root' })
export class ME04LectureCreateService {
  private readonly api = inject(MentorApiService);
  courses() {
    return this.api.request<MentorPage<MentorCourse>>(STUDY_SERVER_APIS.API_046, {
      params: new HttpParams().set('page', 1).set('size', 100),
    });
  }

  upload(file: File, courseId: string) {
    const body = new FormData();
    body.append('file', file);
    body.append('purpose', 'LECTURE');
    body.append('course_id', courseId);
    return this.api.request<MentorUploadAsset>(STUDY_SERVER_APIS.API_034, { body });
  }

  create(
    courseId: string,
    payload: { title: string; content: string; asset_refs: string; order: number },
  ) {
    return this.api.request<MentorLecture>(STUDY_SERVER_APIS.API_047, {
      pathParams: { course_id: courseId },
      body: payload,
    });
  }
}
