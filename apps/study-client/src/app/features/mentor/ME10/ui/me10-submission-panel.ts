import { Component, EventEmitter, Input, Output } from '@angular/core';

import { type SubmissionDetailDto, formatBytes } from '../models/me10-grading.models';

@Component({
  selector: 'study-me10-submission-panel',
  styleUrl: './me10-submission-panel.css',
  templateUrl: './me10-submission-panel.html',
})
export class Me10SubmissionPanel {
  @Input() submission: SubmissionDetailDto | null = null;
  @Input() refreshing = false;

  @Output() readonly refreshDetail = new EventEmitter<void>();

  formatSize(bytes: number): string {
    return formatBytes(bytes);
  }
}
