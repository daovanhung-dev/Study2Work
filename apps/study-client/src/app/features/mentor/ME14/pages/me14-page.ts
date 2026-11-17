import { Component, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

interface RecipientHandoff { id: string; full_name: string }

@Component({ imports: [RouterLink, MentorPageHeader], selector: 'study-me14-page', styleUrls: ['./me14-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me14-page.html' })
export class ME14Page implements OnInit {
  readonly courseId = signal('');
  readonly recipients = signal<RecipientHandoff[]>([]);
  ngOnInit(): void {
    const state = typeof history === 'undefined' ? {} : history.state as { courseId?: unknown; recipients?: unknown };
    if (typeof state.courseId === 'string') this.courseId.set(state.courseId);
    if (Array.isArray(state.recipients)) {
      this.recipients.set(state.recipients.flatMap((item: unknown) => {
        if (!item || typeof item !== 'object') return [];
        const candidate = item as Record<string, unknown>;
        return typeof candidate['id'] === 'string' && typeof candidate['full_name'] === 'string'
          ? [{ id: candidate['id'], full_name: candidate['full_name'] }]
          : [];
      }));
    }
  }
}
