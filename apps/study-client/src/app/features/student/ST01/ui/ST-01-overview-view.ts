import type { Achievement, EnrolledCourse, OverviewWidget, OverviewWidgetKey, StudentNotification } from '../models/ST-01-overview.models';
import { ChangeDetectionStrategy, Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'study-student-overview-view',
  imports: [CommonModule],
  templateUrl: './ST-01-overview-view.html',
  styleUrl: './ST-01-overview-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentOverviewView {
  @Input({ required: true }) courses!: OverviewWidget<EnrolledCourse>;
  @Input({ required: true }) progress!: OverviewWidget<never>;
  @Input({ required: true }) achievements!: OverviewWidget<Achievement>;
  @Input({ required: true }) notifications!: OverviewWidget<StudentNotification>;
  @Input({ required: true }) statusLabel!: string;
  @Output() retry = new EventEmitter<OverviewWidgetKey>();

  statusText<T>(widget: OverviewWidget<T>): string {
    switch (widget.kind) {
      case 'loading': return 'Đang tải';
      case 'ready': return 'Có dữ liệu';
      case 'empty': return 'Danh sách rỗng';
      case 'contract-gap': return 'Thiếu dữ liệu';
      case 'error': return 'Lỗi tải';
    }
  }
}
