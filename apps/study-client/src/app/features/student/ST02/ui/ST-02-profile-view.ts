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
  @Input() state: StudentProfileState = 'loading';
  @Input() profile: StudentProfileDto | null = null;
  @Output() readonly retry = new EventEmitter<void>();
}
