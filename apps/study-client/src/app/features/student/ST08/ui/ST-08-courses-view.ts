import type { StudentCoursesState } from '../models/ST-08-courses.models';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'study-student-courses-view',
  imports: [CommonModule],
  templateUrl: './ST-08-courses-view.html',
  styleUrl: './ST-08-courses-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentCoursesView {
  @Input({ required: true }) state!: StudentCoursesState;
}
