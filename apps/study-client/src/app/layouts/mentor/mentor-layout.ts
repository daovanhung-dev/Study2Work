import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { finalize } from 'rxjs';

import { MentorSessionError, MentorSessionService } from '../../core/auth/mentor-session.service';

@Component({
  imports: [RouterLink, RouterLinkActive, RouterOutlet],
  selector: 'study-mentor-layout',
  styleUrl: './mentor-layout.css',
  templateUrl: './mentor-layout.html',
})
export class MentorLayout {
  readonly session = inject(MentorSessionService);
  readonly isSigningIn = signal(false);
  readonly signInError = signal<string | null>(null);

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
      .subscribe({ error: (error: unknown) => this.signInError.set(getSignInErrorMessage(error)) });
  }

  signOut(): void {
    this.session.endLocalSession();
  }
}

function getSignInErrorMessage(error: unknown): string {
  if (error instanceof MentorSessionError && error.code === 'MENTOR_ROLE_REQUIRED') {
    return 'Tài khoản này không có quyền Mentor.';
  }
  if (error instanceof HttpErrorResponse) {
    if (error.status === 401) return 'Email hoặc mật khẩu không đúng.';
    if (error.status === 403) return 'Tài khoản không được phép đăng nhập.';
    if (error.status === 422) return 'Email hoặc mật khẩu chưa hợp lệ.';
    if (error.status === 0) return 'Không thể kết nối tới Study Server.';
  }
  return 'Không thể đăng nhập lúc này. Vui lòng thử lại.';
}
