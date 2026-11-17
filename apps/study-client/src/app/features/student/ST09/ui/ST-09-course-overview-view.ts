import type { StudentCourseOverviewState } from '../models/ST-09-course-overview.models';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'study-student-course-overview-view',
  imports: [CommonModule],
  templateUrl: './ST-09-course-overview-view.html',
  styleUrl: './ST-09-course-overview-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentCourseOverviewView {
  @Input({ required: true }) state!: StudentCourseOverviewState;
}
