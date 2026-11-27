import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, computed, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { ST03ProfileService } from '../data-access/st03-profile.service';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import { isSafeHttpUrl, isStudentProfile } from '../../shared/models/student-profile.guard';
import { ST03ProfileAvatarPanel } from '../ui/st03-profile-avatar-panel';
import { ST03ProfileDetailsForm } from '../ui/st03-profile-details-form';
import { ST03ProfileFrame } from '../ui/st03-profile-frame';
import type { StudentProfile } from '../../shared/models/student-api.models';

const MAX_AVATAR_BYTES = 5 * 1024 * 1024;
const ALLOWED_AVATAR_TYPES = new Set(['image/png', 'image/jpeg', 'image/webp']);

@Component({
  imports: [RouterLink, ST03ProfileFrame, ST03ProfileAvatarPanel, ST03ProfileDetailsForm],
  selector: 'study-st03-page',
  styleUrl: './st03-page.css',
  templateUrl: './st03-page.html',
})
export class ST03Page implements OnInit {
  private readonly data = inject(ST03ProfileService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly router = inject(Router);
  readonly profileLoading = signal(true);
  readonly profileError = signal<string | null>(null);
  readonly profile = signal<StudentProfile | null>(null);
  readonly fullName = signal('');
  readonly phone = signal('');
  readonly selectedAvatarDataUrl = signal<string | null>(null);
  readonly avatarPreviewUrl = signal<string | null>(null);
  readonly pendingAvatarUrl = signal<string | null>(null);
  readonly avatarUploadState = signal<
    'idle' | 'reading' | 'ready' | 'uploading' | 'uploaded' | 'error'
  >('idle');
  readonly avatarError = signal<string | null>(null);
  readonly saving = signal(false);
  readonly refreshingAfterSave = signal(false);
  readonly savedAwaitingRefresh = signal(false);
  readonly saveError = signal<string | null>(null);
  readonly canSave = computed(() => {
    const profile = this.profile();
    if (
      !profile ||
      this.profileLoading() ||
      this.saving() ||
      this.refreshingAfterSave() ||
      this.savedAwaitingRefresh()
    ) return false;
    if (['reading', 'ready', 'uploading'].includes(this.avatarUploadState())) return false;
    const nextAvatarUrl = this.pendingAvatarUrl() ?? profile.avatar_url;
    return (
      this.fullName().trim() !== profile.full_name ||
      normalizePhone(this.phone()) !== profile.phone ||
      nextAvatarUrl !== profile.avatar_url ||
      this.avatarUploadState() === 'uploaded'
    );
  });

  ngOnInit(): void {
    this.loadProfile();
  }

  retryProfile(): void {
    this.loadProfile(this.savedAwaitingRefresh());
  }

  private loadProfile(afterSave = false): void {
    this.profileLoading.set(true);
    this.refreshingAfterSave.set(afterSave);
    this.profileError.set(null);
    this.data
      .profile()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          if (
            !response.success ||
            response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
            !isStudentProfile(response.data)
          ) {
            this.profileError.set('Chưa thể tải hồ sơ học viên. Vui lòng thử lại.');
            this.profileLoading.set(false);
            this.refreshingAfterSave.set(false);
            return;
          }

          this.setProfile(response.data);
          this.profileLoading.set(false);
          this.refreshingAfterSave.set(false);
          if (afterSave) {
            this.savedAwaitingRefresh.set(false);
            void this.router.navigate(['/student/profile']);
          }
        },
        error: (error: unknown) => {
          this.profileError.set(studentApiErrorMessage(error));
          this.profileLoading.set(false);
          this.refreshingAfterSave.set(false);
        },
      });
  }

  setFullName(event: Event): void {
    this.fullName.set((event.currentTarget as HTMLInputElement).value);
    this.saveError.set(null);
  }

  setPhone(event: Event): void {
    this.phone.set((event.currentTarget as HTMLInputElement).value);
    this.saveError.set(null);
  }

  selectAvatar(event: Event): void {
    const input = event.currentTarget as HTMLInputElement;
    const file = input.files?.[0];
    input.value = '';
    if (!file) return;

    this.avatarError.set(null);
    this.pendingAvatarUrl.set(null);
    if (!ALLOWED_AVATAR_TYPES.has(file.type)) {
      this.avatarUploadState.set('error');
      this.avatarError.set('Chỉ hỗ trợ ảnh PNG, JPEG hoặc WebP.');
      return;
    }
    if (file.size === 0 || file.size > MAX_AVATAR_BYTES) {
      this.avatarUploadState.set('error');
      this.avatarError.set('Ảnh phải lớn hơn 0 và không vượt quá 5 MiB.');
      return;
    }

    this.avatarUploadState.set('reading');
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result !== 'string' || !reader.result.startsWith(`data:${file.type};base64,`)) {
        this.avatarUploadState.set('error');
        this.avatarError.set('Không thể đọc ảnh đã chọn. Vui lòng chọn lại tệp.');
        return;
      }
      this.selectedAvatarDataUrl.set(reader.result);
      this.avatarPreviewUrl.set(reader.result);
      this.avatarUploadState.set('ready');
    };
    reader.onerror = () => {
      this.avatarUploadState.set('error');
      this.avatarError.set('Không thể đọc ảnh đã chọn. Vui lòng chọn lại tệp.');
    };
    reader.readAsDataURL(file);
  }

  uploadAvatar(): void {
    const image = this.selectedAvatarDataUrl();
    if (!image || this.avatarUploadState() !== 'ready') return;

    this.avatarUploadState.set('uploading');
    this.avatarError.set(null);
    this.data
      .uploadAvatar(image)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          const avatarUrl = response.data?.avatar_url;
          if (
            !response.success ||
            response.businessCode !== 'DESIGN_RESOURCE_CREATED' ||
            !isSafeHttpUrl(avatarUrl)
          ) {
            this.avatarUploadState.set('error');
            this.avatarError.set('Hệ thống chưa trả về ảnh đại diện hợp lệ.');
            return;
          }

          this.pendingAvatarUrl.set(avatarUrl);
          this.avatarPreviewUrl.set(avatarUrl);
          this.avatarUploadState.set('uploaded');
        },
        error: (error: unknown) => {
          this.avatarUploadState.set('error');
          this.avatarError.set(studentApiErrorMessage(error));
        },
      });
  }

  saveProfile(event: SubmitEvent): void {
    event.preventDefault();
    const profile = this.profile();
    if (!profile || this.profileLoading() || this.saving() || this.refreshingAfterSave() || this.savedAwaitingRefresh()) return;

    const fullName = this.fullName().trim();
    const nextPhone = normalizePhone(this.phone());
    if (!fullName || fullName.length > 150) {
      this.saveError.set('Họ và tên phải có từ 1 đến 150 ký tự.');
      return;
    }
    if (nextPhone !== null && nextPhone.length > 20) {
      this.saveError.set('Số điện thoại không được vượt quá 20 ký tự.');
      return;
    }
    if (['reading', 'ready', 'uploading'].includes(this.avatarUploadState())) {
      this.saveError.set('Hãy tải ảnh đại diện đã chọn lên trước khi lưu hồ sơ.');
      return;
    }

    this.saving.set(true);
    this.saveError.set(null);
    this.data
      .updateProfile({
        full_name: fullName,
        phone: nextPhone,
        avatar_url: this.pendingAvatarUrl() ?? profile.avatar_url,
      })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          this.saving.set(false);
          if (
            !response.success ||
            response.businessCode !== 'DESIGN_RESOURCE_UPDATED' ||
            !isStudentProfile(response.data)
          ) {
            this.saveError.set('Chưa thể lưu thay đổi hồ sơ. Vui lòng thử lại.');
            return;
          }

          this.setProfile(response.data);
          this.savedAwaitingRefresh.set(true);
          this.loadProfile(true);
        },
        error: (error: unknown) => {
          this.saving.set(false);
          this.saveError.set(studentApiErrorMessage(error));
        },
      });
  }

  private setProfile(profile: StudentProfile): void {
    this.profile.set(profile);
    this.fullName.set(profile.full_name);
    this.phone.set(profile.phone ?? '');
    this.pendingAvatarUrl.set(null);
    this.selectedAvatarDataUrl.set(null);
    this.avatarPreviewUrl.set(
      profile.avatar_url && isSafeHttpUrl(profile.avatar_url) ? profile.avatar_url : null,
    );
    this.avatarUploadState.set('idle');
  }
}

function normalizePhone(value: string): string | null {
  const trimmed = value.trim();
  return trimmed || null;
}
