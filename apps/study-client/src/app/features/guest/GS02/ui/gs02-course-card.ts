import { Component, Input } from '@angular/core';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import type { GS02Course } from '../models/gs02-search.models';

@Component({
  imports: [StudyIcon],
  selector: 'study-gs02-course-card',
  styleUrl: './gs02-course-card.css',
  templateUrl: './gs02-course-card.html',
})
export class GS02CourseCard {
  @Input({ required: true }) course!: GS02Course;
}
