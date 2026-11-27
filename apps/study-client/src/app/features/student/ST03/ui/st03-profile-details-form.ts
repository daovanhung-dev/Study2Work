import { Component, EventEmitter, Input, Output } from '@angular/core';
import { RouterLink } from '@angular/router';

import type { StudentProfile } from '../../shared/models/student-api.models';

@Component({
  imports: [RouterLink],
  selector: 'study-st03-profile-details-form',
  styleUrl: './st03-profile-details-form.css',
  templateUrl: './st03-profile-details-form.html',
})
export class ST03ProfileDetailsForm {
  @Input() profile: StudentProfile | null = null;
  @Input() profileLoading = true;
  @Input() profileError: string | null = null;
  @Input() fullName = '';
  @Input() phone = '';
  @Input() saving = false;
  @Input() refreshingAfterSave = false;
  @Input() savedAwaitingRefresh = false;
  @Input() canSave = false;
  @Input() saveError: string | null = null;

  @Output() fullNameChanged = new EventEmitter<Event>();
  @Output() phoneChanged = new EventEmitter<Event>();
  @Output() retryRequested = new EventEmitter<void>();
  @Output() saveSubmitted = new EventEmitter<SubmitEvent>();
}
