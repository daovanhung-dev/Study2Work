import { Injectable, inject } from '@angular/core';
import { StudentAccountProfileService } from '../../data-access/student-profile.service';

@Injectable({ providedIn: 'root' })
export class StudentProfileService {
  private readonly profile = inject(StudentAccountProfileService);

  getProfile() {
    return this.profile.getProfile();
  }
}
