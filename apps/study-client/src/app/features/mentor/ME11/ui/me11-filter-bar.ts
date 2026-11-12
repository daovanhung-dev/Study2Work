import { Component, EventEmitter, Input, Output } from '@angular/core';

import {
  type Me11CourseOptionDto,
  type SupportStatusCountsVm,
} from '../models/me11-support.models';

@Component({
  selector: 'study-me11-filter-bar',
  styleUrl: './me11-filter-bar.css',
  templateUrl: './me11-filter-bar.html',
})
export class Me11FilterBar {
  @Input() courses: readonly Me11CourseOptionDto[] = [];
  @Input() coursesLoading = false;
  @Input() selectedCourseId: number | null = null;
  @Input() selectedStatus = '';
  @Input() counts: SupportStatusCountsVm = { total: 0, openCount: 0, resolvedCount: 0 };
  @Input() loading = false;

  @Output() readonly statusChange = new EventEmitter<string>();
  @Output() readonly courseChange = new EventEmitter<number | null>();
  @Output() readonly refreshInbox = new EventEmitter<void>();

  readonly statusTabs = [
    { value: '', label: 'Tất cả' },
    { value: 'OPEN', label: 'Đang mở (OPEN)' },
    { value: 'IN_PROGRESS', label: 'Đang xử lý (IN_PROGRESS)' },
    { value: 'WAITING_LEARNER', label: 'Chờ học viên (WAITING_LEARNER)' },
    { value: 'RESOLVED', label: 'Đã giải quyết (RESOLVED)' },
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
}
