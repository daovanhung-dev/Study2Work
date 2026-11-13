import { Component, EventEmitter, Input, Output } from '@angular/core';

import {
  type SubmissionItemDto,
  type SubmissionPaginationDto,
  formatSubmissionStatus,
} from '../models/me09-submissions.models';

@Component({
  selector: 'study-me09-submission-list',
  styleUrl: './me09-submission-list.css',
  templateUrl: './me09-submission-list.html',
})
export class Me09SubmissionList {
  @Input() items: readonly SubmissionItemDto[] = [];
  @Input() pagination: SubmissionPaginationDto = {
    page: 1,
    size: 20,
    total: 0,
    total_pages: 0,
  };

  @Output() readonly openSubmission = new EventEmitter<number>();
  @Output() readonly pageChange = new EventEmitter<number>();

  statusLabel(status: string): string {
    return formatSubmissionStatus(status);
  }

  isGraded(status: string): boolean {
    return status.toUpperCase() === 'GRADED';
  }
}
