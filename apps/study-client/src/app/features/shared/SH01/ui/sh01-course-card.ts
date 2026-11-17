import { Component, input } from '@angular/core';

import type { SH01PublicCourse } from '../models/sh01-catalog.models';

@Component({
  selector: 'study-sh01-course-card',
  styleUrl: './sh01-course-card.css',
  templateUrl: './sh01-course-card.html',
})
export class SH01CourseCard {
  readonly course = input.required<SH01PublicCourse>();
}
