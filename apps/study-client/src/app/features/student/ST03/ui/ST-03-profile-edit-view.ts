import type {
  StudentProfileEditDto,
  StudentProfileEditState,
} from '../models/ST-03-profile-edit.models';
import { ChangeDetectionStrategy, Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'study-student-profile-edit-view',
  imports: [CommonModule],
  templateUrl: './ST-03-profile-edit-view.html',
  styleUrl: './ST-03-profile-edit-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentProfileEditView {
  @Input() state: StudentProfileEditState = 'loading';
  @Input() profile: StudentProfileEditDto | null = null;
  @Output() readonly retry = new EventEmitter<void>();
}
