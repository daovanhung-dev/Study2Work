import { Component, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, NavigationEnd, Router, RouterLink, RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { filter } from 'rxjs';

import {
  StudentSessionError,
  StudentSessionService,
} from '../../core/auth/student-session.service';
import { studentApiErrorMessage } from '../../features/student/shared/models/student-api-errors';

type StudentShellMode = 'legacy' | 'portal' | 'exam' | 'blank' | 'custom';

@Component({
  imports: [FormsModule, RouterLink, RouterOutlet],
  selector: 'study-student-layout',
  styleUrl: './student-layout.css',
  templateUrl: './student-layout.html',
})
export class StudentLayout {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  readonly session = inject(StudentSessionService);
  readonly loginBusy = signal(false);
  readonly loginError = signal<string | null>(null);
  email = '';
  password = '';

  shellMode: StudentShellMode = 'legacy';

  constructor() {
    this.router.events
      .pipe(
        filter((event): event is NavigationEnd => event instanceof NavigationEnd),
        takeUntilDestroyed(),
      )
      .subscribe(() => this.setShellMode());
  }

  setShellMode(): void {
    const shell = this.route.firstChild?.snapshot.data['shell'];
    this.shellMode =
      shell === 'portal' || shell === 'exam' || shell === 'blank' || shell === 'custom'
        ? shell
        : 'legacy';
  }

  login(): void {
    if (this.loginBusy()) return;
    this.loginBusy.set(true);
    this.loginError.set(null);
    this.session.login(this.email.trim(), this.password).subscribe({
      next: () => {
        this.password = '';
        this.loginBusy.set(false);
      },
      error: (error: unknown) => {
        this.loginError.set(
          error instanceof StudentSessionError && error.code === 'STUDENT_ROLE_REQUIRED'
            ? 'Tài khoản này không có vai trò Học viên.'
            : studentApiErrorMessage(error),
        );
        this.loginBusy.set(false);
      },
    });
  }

  logout(): void {
    this.session.endLocalSession();
  }
}
