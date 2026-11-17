import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ME05LectureDetailService } from '../data-access/me05-lecture-detail.service';
import type { MentorLecture } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [RouterLink, MentorPageHeader], selector: 'study-me05-page', styleUrls: ['./me05-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me05-page.html' })
export class ME05Page implements OnInit {
  private readonly data = inject(ME05LectureDetailService);
  private readonly route = inject(ActivatedRoute);
  readonly lecture = signal<MentorLecture | null>(null);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly invalidId = signal(false);
  ngOnInit(): void {
    const id = toSafeMentorId(this.route.snapshot.paramMap.get('lectureId'));
    if (!id) { this.invalidId.set(true); this.loading.set(false); return; }
    this.load(id);
  }
  load(id = this.route.snapshot.paramMap.get('lectureId') ?? ''): void {
    this.loading.set(true); this.error.set(null);
    this.data.detail(id).subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.error.set(issue); else this.lecture.set(response.data); this.loading.set(false); }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.loading.set(false); } });
  }
  safeId(value: unknown): string | null { return toSafeMentorId(value); }
}
