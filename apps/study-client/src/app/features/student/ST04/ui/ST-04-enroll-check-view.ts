import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import type { St04CourseLoadState, St04CourseSummary } from '../models/ST-04-enroll-course.models';

@Component({
  selector: 'study-student-enroll-check-view',
  imports: [CommonModule],
  templateUrl: './ST-04-enroll-check-view.html',
  styleUrl: './ST-04-enroll-check-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentEnrollCheckView {
  @Input() course: St04CourseSummary | null = null;
  @Input() loadState: St04CourseLoadState = 'loading';
}
