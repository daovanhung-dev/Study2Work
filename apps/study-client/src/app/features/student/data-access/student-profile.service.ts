import { Injectable, inject } from '@angular/core';
import { map } from 'rxjs';
import { StudyApiService } from '../../../core/http/study-api.service';
import { STUDY_SERVER_APIS } from '../../../core/constant/api.constants';
import type { StudentAccountProfileDto } from '../models/student-profile.models';

@Injectable({ providedIn: 'root' })
export class StudentAccountProfileService {
  private readonly api = inject(StudyApiService);
  /** API #04. Authentication remains owned by the shared HTTP/session infrastructure. */
  getProfile() {
    return this.api.request<StudentAccountProfileDto>(STUDY_SERVER_APIS.API_004).pipe(
      map((response) => {
        const p = response?.data;
        if (
          response?.success !== true ||
          response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
          !p ||
          !Number.isSafeInteger(p.id) ||
          typeof p.full_name !== 'string' ||
          typeof p.email !== 'string' ||
          typeof p.role !== 'string' ||
          typeof p.status !== 'string' ||
          !(p.avatar_url === null || typeof p.avatar_url === 'string') ||
          !(p.phone === null || typeof p.phone === 'string') ||
          typeof p.created_at !== 'string' ||
          typeof p.updated_at !== 'string'
        ) {
          throw new Error('Invalid Study profile response');
        }
        return p;
      }),
    );
  }
}
