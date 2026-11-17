import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ME11SupportInboxService } from '../data-access/me11-support-inbox.service';
import type { MentorSupportRequest } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [DatePipe, RouterLink, MentorPageHeader], selector: 'study-me11-page', styleUrls: ['./me11-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me11-page.html' })
export class ME11Page implements OnInit {
  private readonly data = inject(ME11SupportInboxService);
  readonly requests = signal<MentorSupportRequest[]>([]);
  readonly courseFilter = signal('');
  readonly statusFilter = signal('');
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  ngOnInit(): void { this.load(); }
  load(courseId = this.courseFilter(), status = this.statusFilter()): void {
    if (courseId && !toSafeMentorId(courseId)) { this.error.set('Course ID cần là số nguyên dương int64.'); return; }
    this.courseFilter.set(courseId); this.statusFilter.set(status); this.loading.set(true); this.error.set(null);
    this.data.list(courseId, status).subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.error.set(issue); else this.requests.set(response.data); this.loading.set(false); }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.loading.set(false); } });
  }
  apply(courseId: string, status: string): void { this.load(courseId.trim(), status.trim()); }
  safeId(value: unknown): string | null { return toSafeMentorId(value); }
  lastMessage(request: MentorSupportRequest): string { return request.messages.at(-1)?.content ?? 'Chưa có tin nhắn.'; }
}
