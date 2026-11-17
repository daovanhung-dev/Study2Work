import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ME02CoursesService } from '../data-access/me02-courses.service';
import type { MentorCourse, MentorPage } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [RouterLink, MentorPageHeader], selector: 'study-me02-page', styleUrls: ['./me02-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me02-page.html' })
export class ME02Page implements OnInit {
  private readonly data = inject(ME02CoursesService);
  readonly courses = signal<MentorCourse[]>([]);
  readonly page = signal(1);
  readonly total = signal(0);
  readonly totalPages = signal(0);
  readonly status = signal('');
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  ngOnInit(): void { this.load(); }
  load(page = this.page(), status = this.status()): void {
    this.page.set(page); this.status.set(status); this.loading.set(true); this.error.set(null);
    this.data.list(page, status).subscribe({
      next: (response) => {
        const issue = mentorEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else { const result = response.data as MentorPage<MentorCourse>; this.courses.set(result.items); this.total.set(result.pagination.total); this.totalPages.set(result.pagination.total_pages); }
        this.loading.set(false);
      }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.loading.set(false); },
    });
  }
  filter(status: string): void { this.load(1, status); }
  safeId(value: unknown): string | null { return toSafeMentorId(value); }
}
