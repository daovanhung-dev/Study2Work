import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminPage, AdminCourse } from '../../admin-api.models';

@Injectable({ providedIn: 'root' })
export class AD09ApiService {
  private readonly api = inject(AdminApiService);

  getCourse(courseId: string) {
    return this.api.get<AdminPage<AdminCourse>>(STUDY_SERVER_APIS.API_074, {
      pathParams: { course_id: courseId },
    });
  }
}
