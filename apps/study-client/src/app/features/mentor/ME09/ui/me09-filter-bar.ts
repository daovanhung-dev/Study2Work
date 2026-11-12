import { Component, EventEmitter, Input, Output } from '@angular/core';

import { type MentorCourseOptionDto } from '../models/me09-submissions.models';

@Component({
  selector: 'study-me09-filter-bar',
  styleUrl: './me09-filter-bar.css',
  templateUrl: './me09-filter-bar.html',
})
export class Me09FilterBar {
  @Input() courses: readonly MentorCourseOptionDto[] = [];
  @Input() coursesLoading = false;
  @Input() selectedCourseId: number | null = null;
  @Input() selectedStatus = '';
  @Input() loading = false;

  @Output() readonly courseChange = new EventEmitter<number | null>();
  @Output() readonly statusChange = new EventEmitter<string>();
  @Output() readonly resetFilters = new EventEmitter<void>();
  @Output() readonly refreshList = new EventEmitter<void>();

  readonly statusOptions = [
    { value: '', label: 'Tất cả trạng thái' },
    { value: 'SUBMITTED', label: 'SUBMITTED (Chờ chấm)' },
    { value: 'GRADED', label: 'GRADED (Đã chấm)' },
  ] as const;

  onCourseSelect(event: Event): void {
    const raw = (event.target as HTMLSelectElement | null)?.value ?? '';
    if (!raw) {
      this.courseChange.emit(null);
      return;
    }
    const parsed = Number(raw);
    this.courseChange.emit(Number.isSafeInteger(parsed) && parsed > 0 ? parsed : null);
  }

  onStatusSelect(event: Event): void {
    const raw = (event.target as HTMLSelectElement | null)?.value ?? '';
    this.statusChange.emit(raw);
  }
}
