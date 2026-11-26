import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

import { StudentSessionService } from '../../core/auth/student-session.service';

@Component({
  imports: [RouterLink, RouterLinkActive],
  selector: 'study-student-public-frame',
  templateUrl: './student-public-frame.html',
  styleUrl: './student-public-frame.css',
})
export class StudentPublicFrame {
  readonly session = inject(StudentSessionService);

  logout(): void {
    this.session.endLocalSession();
  }
}
