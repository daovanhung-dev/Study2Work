import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ME16CourseProgressService } from '../data-access/me16-course-progress.service';
import type { MentorCourseProgressRow, MentorPage } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [RouterLink, MentorPageHeader], selector: 'study-me16-page', styleUrls: ['./me16-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me16-page.html' })
export class ME16Page implements OnInit {
  private readonly data = inject(ME16CourseProgressService);
  private readonly route = inject(ActivatedRoute);
  readonly courseId = signal('');
  readonly rows = signal<MentorCourseProgressRow[]>([]);
  readonly total = signal(0);
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
    this.data.progress(id).subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.error.set(issue); else { const result = response.data as MentorPage<MentorCourseProgressRow>; this.rows.set(result.items); this.total.set(result.pagination.total); } this.loading.set(false); }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.loading.set(false); } });
  }
  safeId(value: unknown): string | null { return toSafeMentorId(value); }
}
