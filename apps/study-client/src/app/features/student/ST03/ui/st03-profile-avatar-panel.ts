import { Component, EventEmitter, Input, Output } from '@angular/core';

import type { StudentProfile } from '../../shared/models/student-api.models';

export type ST03AvatarUploadState =
  | 'idle'
  | 'reading'
  | 'ready'
  | 'uploading'
  | 'uploaded'
  | 'error';

@Component({
  selector: 'study-st03-profile-avatar-panel',
  styleUrl: './st03-profile-avatar-panel.css',
  templateUrl: './st03-profile-avatar-panel.html',
})
export class ST03ProfileAvatarPanel {
  @Input() profileLoading = true;
  @Input() profile: StudentProfile | null = null;
  @Input() avatarPreviewUrl: string | null = null;
  @Input() avatarUploadState: ST03AvatarUploadState = 'idle';
  @Input() avatarError: string | null = null;
  @Input() saving = false;
  @Input() refreshingAfterSave = false;
  @Input() savedAwaitingRefresh = false;

  @Output() avatarFileSelected = new EventEmitter<Event>();
  @Output() uploadRequested = new EventEmitter<void>();
}
