import { Component, input, signal } from '@angular/core';

import type { SH01PublicCourse } from '../models/sh01-catalog.models';

@Component({
  selector: 'study-sh01-course-card',
  styleUrl: './sh01-course-card.css',
  templateUrl: './sh01-course-card.html',
})
export class SH01CourseCard {
  readonly course = input.required<SH01PublicCourse>();
  private readonly failedMentorAvatarUrl = signal<string | null>(null);
  private readonly failedThumbnailUrl = signal<string | null>(null);

  hasThumbnail(): boolean {
    const thumbnailUrl = this.course().thumbnail_url;
    return Boolean(thumbnailUrl) && this.failedThumbnailUrl() !== thumbnailUrl;
  }

  onThumbnailError(): void {
    this.failedThumbnailUrl.set(this.course().thumbnail_url ?? null);
  }

  hasMentorAvatar(): boolean {
    const avatarUrl = this.course().mentor.avatar_url;
    return Boolean(avatarUrl) && this.failedMentorAvatarUrl() !== avatarUrl;
  }

  onMentorAvatarError(): void {
    this.failedMentorAvatarUrl.set(this.course().mentor.avatar_url ?? null);
  }
}
