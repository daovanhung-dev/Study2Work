import { Injectable, inject } from '@angular/core';
import { HttpParams } from '@angular/common/http';
import { StudyApiService } from '../../../../core/http/study-api.service';
import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { StudentCoursesPageData } from '../models/ST-08-courses.models';

@Injectable({ providedIn: 'root' })
export class StudentCoursesService {
  private readonly api = inject(StudyApiService);

  getCourses(page = 1) {
    return this.api.request<StudentCoursesPageData>(STUDY_SERVER_APIS.API_020, {
      params: new HttpParams().set('page', page),
    });
  }
}
