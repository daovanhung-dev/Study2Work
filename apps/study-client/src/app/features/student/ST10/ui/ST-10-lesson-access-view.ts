import type { StudentLessonAccessState } from '../models/ST-10-lesson-access.models';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'study-student-lesson-access-view',
  imports: [CommonModule],
  templateUrl: './ST-10-lesson-access-view.html',
  styleUrl: './ST-10-lesson-access-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentLessonAccessView {
  @Input({ required: true }) state!: StudentLessonAccessState;
}
