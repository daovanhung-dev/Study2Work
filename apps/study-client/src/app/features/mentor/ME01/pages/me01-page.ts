import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ME01DashboardService } from '../data-access/me01-dashboard.service';
import type { MentorCourse, MentorSubmission, MentorSupportRequest } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({
  imports: [DatePipe, RouterLink, MentorPageHeader],
  selector: 'study-me01-page',
  styleUrls: ['./me01-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me01-page.html',
})
export class ME01Page implements OnInit {
  private readonly data = inject(ME01DashboardService);
  readonly courses = signal<MentorCourse[]>([]);
  readonly submissions = signal<MentorSubmission[]>([]);
  readonly supportRequests = signal<MentorSupportRequest[]>([]);
  readonly courseLoading = signal(true);
  readonly submissionLoading = signal(true);
  readonly supportLoading = signal(true);
  readonly courseError = signal<string | null>(null);
  readonly submissionError = signal<string | null>(null);
  readonly supportError = signal<string | null>(null);

  ngOnInit(): void { this.load(); }

  load(): void {
    this.courseLoading.set(true); this.courseError.set(null);
    this.data.courses().subscribe({
      next: (response) => {
        const issue = mentorEnvelopeError(response.success, response.message);
        if (issue) this.courseError.set(issue); else this.courses.set(response.data.items);
        this.courseLoading.set(false);
      },
      error: (error: unknown) => { this.courseError.set(mentorApiErrorMessage(error)); this.courseLoading.set(false); },
    });
    this.submissionLoading.set(true); this.submissionError.set(null);
    this.data.submissions().subscribe({
      next: (response) => {
        const issue = mentorEnvelopeError(response.success, response.message);
        if (issue) this.submissionError.set(issue); else this.submissions.set(response.data.items);
        this.submissionLoading.set(false);
      },
      error: (error: unknown) => { this.submissionError.set(mentorApiErrorMessage(error)); this.submissionLoading.set(false); },
    });
    this.supportLoading.set(true); this.supportError.set(null);
    this.data.support().subscribe({
      next: (response) => {
        const issue = mentorEnvelopeError(response.success, response.message);
        if (issue) this.supportError.set(issue); else this.supportRequests.set(response.data);
        this.supportLoading.set(false);
      },
      error: (error: unknown) => { this.supportError.set(mentorApiErrorMessage(error)); this.supportLoading.set(false); },
    });
  }

  safeId(value: unknown): string | null { return toSafeMentorId(value); }
  lastMessage(request: MentorSupportRequest): string { return request.messages.at(-1)?.content ?? 'Chưa có nội dung trao đổi.'; }
}
