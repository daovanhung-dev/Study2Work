import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import type {
  St05CourseLoadState,
  St05CourseSummary,
} from '../models/ST-05-checkout-course.models';

@Component({
  selector: 'study-student-order-check-view',
  imports: [CommonModule],
  templateUrl: './ST-05-order-check-view.html',
  styleUrl: './ST-05-order-check-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentOrderCheckView {
  @Input() course: St05CourseSummary | null = null;
  @Input() loadState: St05CourseLoadState = 'loading';
  @Input() backToEnrollUrl = '/student';
}
