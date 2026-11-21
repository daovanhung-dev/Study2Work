import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

import { ST02ProfileService } from '../data-access/st02-profile.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentProfile } from '../../shared/models/student-api.models';
import { isSafeHttpUrl, isStudentProfile } from '../../shared/models/student-profile.guard';

@Component({
  imports: [RouterLink, RouterLinkActive],
  selector: 'study-st02-page',
  templateUrl: './st02-page.html',
})
export class ST02Page implements OnInit {
  private readonly data = inject(ST02ProfileService);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly profile = signal<StudentProfile | null>(null);

  ngOnInit(): void {
    this.loadProfile();
  }

  retry(): void {
    this.loadProfile();
  }

  avatarUrl(): string | null {
    const value = this.profile()?.avatar_url;
    return isSafeHttpUrl(value) ? value : null;
  }

  roleLabel(): string {
    const role = this.profile()?.role.trim().toUpperCase();
    return role === 'STUDENT' ? 'Học viên' : 'Chưa xác định';
  }

  statusLabel(): string {
    const status = this.profile()?.status.trim().toUpperCase();
    if (status === 'ACTIVE') return 'Đang hoạt động';
    if (status === 'SUSPENDED') return 'Tạm khóa';
    return 'Chưa xác định';
  }

  private loadProfile(): void {
    this.loading.set(true);
    this.error.set(null);
    this.data.profile().subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else if (
          response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
          !isStudentProfile(response.data)
        ) {
          this.error.set('Chưa thể tải thông tin hồ sơ. Vui lòng thử lại.');
        } else this.profile.set(response.data);
        this.loading.set(false);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.loading.set(false);
      },
    });
  }
}
