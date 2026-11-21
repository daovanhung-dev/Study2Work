import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentProfile } from '../../shared/models/student-api.models';

export interface StudentProfileUpdateRequest {
  full_name: string;
  phone: string | null;
  avatar_url: string | null;
}

export interface StudentAvatarUploadResult {
  avatar_url: string;
}

@Injectable({ providedIn: 'root' })
export class ST03ProfileService {
  private readonly api = inject(StudentApiService);

  profile() {
    return this.api.request<StudentProfile>(STUDY_SERVER_APIS.API_004);
  }

  uploadAvatar(image: string) {
    return this.api.request<StudentAvatarUploadResult>(STUDY_SERVER_APIS.API_013, {
      body: { image },
    });
  }

  updateProfile(profile: StudentProfileUpdateRequest) {
    return this.api.request<StudentProfile>(STUDY_SERVER_APIS.API_014, {
      body: profile,
    });
  }
}
