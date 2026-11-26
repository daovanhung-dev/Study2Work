import { Component, Input, OnChanges, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import type { GS02Course } from '../models/gs02-search.models';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-gs02-course-card',
  styleUrl: './gs02-course-card.css',
  templateUrl: './gs02-course-card.html',
})
export class GS02CourseCard implements OnChanges {
  @Input({ required: true }) course!: GS02Course;

  readonly imageFailed = signal(false);
  private lastThumbnailUrl: string | null = null;

  ngOnChanges(): void {
    const nextUrl = this.course?.thumbnail_url ?? null;
    if (nextUrl !== this.lastThumbnailUrl) {
      this.lastThumbnailUrl = nextUrl;
      this.imageFailed.set(false);
    }
  }

  onImageError(): void {
    this.imageFailed.set(true);
  }
}
