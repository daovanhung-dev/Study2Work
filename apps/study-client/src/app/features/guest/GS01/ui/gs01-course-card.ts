import { Component, Input, OnChanges, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import type { GuestPublicCourse } from '../../shared/models/guest-course.models';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-gs01-course-card',
  styleUrl: './gs01-course-card.css',
  templateUrl: './gs01-course-card.html',
})
export class GS01CourseCard implements OnChanges {
  @Input({ required: true }) course!: GuestPublicCourse;

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
