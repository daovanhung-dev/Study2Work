import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import type { GuestPublicCourse } from '../../shared/models/guest-course.models';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-gs01-course-card',
  styleUrl: './gs01-course-card.css',
  templateUrl: './gs01-course-card.html',
})
export class GS01CourseCard {
  @Input({ required: true }) course!: GuestPublicCourse;
}
