import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ME09SubmissionsService } from '../data-access/me09-submissions.service';
import type { MentorPage, MentorSubmission } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [DatePipe, RouterLink, MentorPageHeader], selector: 'study-me09-page', styleUrls: ['./me09-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me09-page.html' })
export class ME09Page implements OnInit {
  private readonly data = inject(ME09SubmissionsService);
  readonly submissions = signal<MentorSubmission[]>([]);
  readonly page = signal(1);
  readonly total = signal(0);
  readonly totalPages = signal(0);
  readonly courseFilter = signal('');
  readonly statusFilter = signal('');
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  ngOnInit(): void { this.load(); }
  load(page = this.page(), courseId = this.courseFilter(), status = this.statusFilter()): void {
    if (courseId && !toSafeMentorId(courseId)) { this.error.set('Course ID cần là số nguyên dương int64.'); return; }
    this.page.set(page); this.courseFilter.set(courseId); this.statusFilter.set(status); this.loading.set(true); this.error.set(null);
    this.data.list(page, courseId, status).subscribe({
      next: (response) => {
        const issue = mentorEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else { const result = response.data as MentorPage<MentorSubmission>; this.submissions.set(result.items); this.total.set(result.pagination.total); this.totalPages.set(result.pagination.total_pages); }
        this.loading.set(false);
      }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.loading.set(false); },
    });
  }
  applyFilters(courseId: string, status: string): void { this.load(1, courseId.trim(), status.trim()); }
  safeId(value: unknown): string | null { return toSafeMentorId(value); }
}
