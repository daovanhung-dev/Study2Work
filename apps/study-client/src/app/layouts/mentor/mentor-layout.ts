import { Component, inject } from '@angular/core';
import { Router, RouterLink, RouterOutlet } from '@angular/router';

@Component({
  imports: [RouterOutlet, RouterLink],
  selector: 'study-mentor-layout',
  templateUrl: './mentor-layout.html',
  styleUrl: './mentor-layout.css',
})
export class MentorLayout {
  private readonly router = inject(Router);

  isSectionActive(section: 'courses' | 'submissions' | 'support' | 'notifications'): boolean {
    const url = this.router.url;
    if (section === 'courses') {
      return url.includes('/mentor/courses') || url.includes('/mentor/content');
    }
    if (section === 'submissions') {
      return url.includes('/mentor/submissions');
    }
    if (section === 'support') {
      return url.includes('/mentor/support');
    }
    return url.includes('/mentor/notifications');
  }
}
