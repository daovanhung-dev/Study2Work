import { Component, Input } from '@angular/core';

import {
  type LessonProgressStatus,
  type StudentLessonProgressDto,
  formatLessonProgressStatus,
} from '../models/me17-student-progress.models';

@Component({
  selector: 'study-me17-lesson-list',
  styleUrl: './me17-lesson-list.css',
  templateUrl: './me17-lesson-list.html',
})
export class Me17LessonList {
  @Input() lessons: readonly StudentLessonProgressDto[] = [];

  statusLabel(status: LessonProgressStatus): string {
    return formatLessonProgressStatus(status);
  }
}
