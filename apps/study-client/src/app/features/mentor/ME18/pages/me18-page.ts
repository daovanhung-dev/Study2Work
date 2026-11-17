import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ME18AnalyticsService } from '../data-access/me18-analytics.service';
import type { MentorCourseAnalytics } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [DatePipe, RouterLink, MentorPageHeader], selector: 'study-me18-page', styleUrls: ['./me18-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me18-page.html' })
export class ME18Page implements OnInit {
  private readonly data = inject(ME18AnalyticsService);
  private readonly route = inject(ActivatedRoute);
  readonly courseId = signal('');
  readonly analytics = signal<MentorCourseAnalytics | null>(null);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly invalidId = signal(false);
  ngOnInit(): void {
    const id = toSafeMentorId(this.route.snapshot.paramMap.get('courseId'));
    if (!id) { this.invalidId.set(true); this.loading.set(false); return; }
    this.courseId.set(id); this.load(id);
  }
  load(id = this.courseId()): void {
    if (!id) return;
    this.loading.set(true); this.error.set(null);
    this.data.load(id).subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.error.set(issue); else this.analytics.set(response.data); this.loading.set(false); }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.loading.set(false); } });
  }
}
