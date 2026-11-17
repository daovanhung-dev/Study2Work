import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ME10SubmissionReviewService } from '../data-access/me10-submission-review.service';
import type { MentorSubmission } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [DatePipe, RouterLink, MentorPageHeader], selector: 'study-me10-page', styleUrls: ['./me10-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me10-page.html' })
export class ME10Page implements OnInit {
  private readonly data = inject(ME10SubmissionReviewService);
  private readonly route = inject(ActivatedRoute);
  readonly submissionId = signal('');
  readonly submission = signal<MentorSubmission | null>(null);
  readonly loading = signal(true);
  readonly gradeSaving = signal(false);
  readonly feedbackSaving = signal(false);
  readonly gradeError = signal<string | null>(null);
  readonly feedbackError = signal<string | null>(null);
  readonly gradeSuccess = signal<string | null>(null);
  readonly feedbackSuccess = signal<string | null>(null);
  readonly invalidId = signal(false);
  ngOnInit(): void {
    const id = toSafeMentorId(this.route.snapshot.paramMap.get('submissionId'));
    if (!id) { this.invalidId.set(true); this.loading.set(false); return; }
    this.submissionId.set(id); this.load(id);
  }
  load(id = this.submissionId()): void {
    if (!id) return;
    this.loading.set(true); this.gradeError.set(null); this.feedbackError.set(null);
    this.data.detail(id).subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.gradeError.set(issue); else this.submission.set(response.data); this.loading.set(false); }, error: (error: unknown) => { this.gradeError.set(mentorApiErrorMessage(error)); this.loading.set(false); } });
  }
  saveGrade(event: SubmitEvent, scoreText: string): void {
    event.preventDefault();
    const score = Number(scoreText);
    if (!Number.isSafeInteger(score) || score < 0) { this.gradeError.set('Điểm cần là số nguyên không âm. Assignment max_score được Study Server xác thực.'); return; }
    this.gradeSaving.set(true); this.gradeError.set(null); this.gradeSuccess.set(null);
    this.data.grade(this.submissionId(), score, '').subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.gradeError.set(issue); else { this.submission.set(response.data); this.gradeSuccess.set('Điểm đã được Study Server ghi nhận.'); } this.gradeSaving.set(false); }, error: (error: unknown) => { this.gradeError.set(mentorApiErrorMessage(error)); this.gradeSaving.set(false); } });
  }
  sendFeedback(event: SubmitEvent, text: string): void {
    event.preventDefault();
    if (!text.trim()) { this.feedbackError.set('Nhận xét không được để trống.'); return; }
    this.feedbackSaving.set(true); this.feedbackError.set(null); this.feedbackSuccess.set(null);
    this.data.feedback(this.submissionId(), text, '[]').subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.feedbackError.set(issue); else { this.submission.set(response.data); this.feedbackSuccess.set('Nhận xét đã được Study Server lưu.'); } this.feedbackSaving.set(false); }, error: (error: unknown) => { this.feedbackError.set(mentorApiErrorMessage(error)); this.feedbackSaving.set(false); } });
  }
}
