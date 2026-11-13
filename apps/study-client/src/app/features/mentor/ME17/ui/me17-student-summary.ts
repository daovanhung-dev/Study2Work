import { Component, Input } from '@angular/core';

import { type StudentCourseProgressDto } from '../models/me17-student-progress.models';

@Component({
  selector: 'study-me17-student-summary',
  styleUrl: './me17-student-summary.css',
  templateUrl: './me17-student-summary.html',
})
export class Me17StudentSummary {
  @Input() progressData: StudentCourseProgressDto | null = null;
}
