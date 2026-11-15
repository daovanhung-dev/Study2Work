import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { Router, RouterLink, RouterOutlet } from '@angular/router';
import { finalize } from 'rxjs';

import { AdminSessionError, AdminSessionService } from '../../core/auth/admin-session.service';
import { StudyIcon } from '../../shared/ui/study-icon';

@Component({
  imports: [RouterLink, RouterOutlet, StudyIcon],
  selector: 'study-admin-layout',
  styleUrl: './admin-layout.css',
  templateUrl: './admin-layout.html',
})
export class AdminLayout {
  readonly session = inject(AdminSessionService);
  readonly isSigningIn = signal(false);
  readonly signInError = signal<string | null>(null);

  constructor(readonly router: Router) {}

  signIn(event: Event, email: string, password: string): void {
    event.preventDefault();
    if (this.isSigningIn()) {
      return;
    }

    this.signInError.set(null);
    this.isSigningIn.set(true);
    this.session
      .login(email, password)
      .pipe(finalize(() => this.isSigningIn.set(false)))
      .subscribe({
        error: (error: unknown) => this.signInError.set(getSignInErrorMessage(error)),
      });
  }

  signOut(): void {
    this.session.endLocalSession();
  }

  get isUsersRoute(): boolean {
    return this.router.url.startsWith('/admin/users');
  }

  get isCoursesRoute(): boolean {
    return /\/admin\/(courses|lessons|quizzes)(\/|\?|#|$)/.test(this.router.url);
  }

  get isNotificationsRoute(): boolean {
    return this.router.url.startsWith('/admin/notifications');
  }

  get isModerationRoute(): boolean {
    return this.router.url.startsWith('/admin/content') || this.router.url.startsWith('/admin/discussions');
  }

  get isReportsRoute(): boolean {
    return this.router.url.startsWith('/admin/reports');
  }

  get isAdminHome(): boolean {
    return this.router.url === '/admin' || this.router.url === '/admin/';
  }

}

function getSignInErrorMessage(error: unknown): string {
  if (error instanceof AdminSessionError && error.code === 'ADMIN_ROLE_REQUIRED') {
    return 'Tài khoản này không có quyền quản trị.';
  }
  if (error instanceof HttpErrorResponse) {
    if (error.status === 401) {
      return 'Email hoặc mật khẩu không đúng.';
    }
    if (error.status === 403) {
      return 'Tài khoản không được phép đăng nhập.';
    }
    if (error.status === 422) {
      return 'Email hoặc mật khẩu chưa hợp lệ.';
    }
    if (error.status === 0) {
      return 'Không thể kết nối tới Study Server.';
    }
  }
  return 'Không thể đăng nhập lúc này. Vui lòng thử lại.';
}
