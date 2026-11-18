import type { StudentProfileDto, StudentProfileState } from '../models/ST-02-profile.models';
import { ChangeDetectionStrategy, Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'study-student-profile-view',
  imports: [CommonModule],
  templateUrl: './ST-02-profile-view.html',
  styleUrl: './ST-02-profile-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentProfileView {
  avatarFailed = false;
  private currentProfile: StudentProfileDto | null = null;
  @Input() state: StudentProfileState = 'loading';
  @Input() set profile(value: StudentProfileDto | null) {
    if (value !== this.currentProfile) this.avatarFailed = false;
    this.currentProfile = value;
  }
  get profile(): StudentProfileDto | null {
    return this.currentProfile;
  }
  @Output() readonly retry = new EventEmitter<void>();
}
