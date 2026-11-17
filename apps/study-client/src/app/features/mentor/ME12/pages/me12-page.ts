import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ME12SupportThreadService } from '../data-access/me12-support-thread.service';
import type { MentorSupportRequest } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [DatePipe, RouterLink, MentorPageHeader], selector: 'study-me12-page', styleUrls: ['./me12-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me12-page.html' })
export class ME12Page implements OnInit {
  private readonly data = inject(ME12SupportThreadService);
  private readonly route = inject(ActivatedRoute);
  readonly requestId = signal('');
  readonly request = signal<MentorSupportRequest | null>(null);
  readonly loading = signal(true);
  readonly sending = signal(false);
  readonly resolving = signal(false);
  readonly error = signal<string | null>(null);
  readonly actionError = signal<string | null>(null);
  readonly actionSuccess = signal<string | null>(null);
  readonly confirmResolve = signal(false);
  readonly invalidId = signal(false);
  ngOnInit(): void {
    const id = toSafeMentorId(this.route.snapshot.paramMap.get('requestId'));
    if (!id) { this.invalidId.set(true); this.loading.set(false); return; }
    this.requestId.set(id); this.load(id);
  }
  load(id = this.requestId()): void {
    if (!id) return;
    this.loading.set(true); this.error.set(null);
    this.data.detail(id).subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.error.set(issue); else this.request.set(response.data); this.loading.set(false); }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.loading.set(false); } });
  }
  reply(event: SubmitEvent, message: string): void {
    event.preventDefault();
    if (!message.trim()) { this.actionError.set('Câu trả lời không được để trống.'); return; }
    this.sending.set(true); this.actionError.set(null); this.actionSuccess.set(null);
    this.data.reply(this.requestId(), message).subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.actionError.set(issue); else { this.request.set(response.data); this.actionSuccess.set('Câu trả lời đã được thêm vào thread.'); } this.sending.set(false); }, error: (error: unknown) => { this.actionError.set(mentorApiErrorMessage(error)); this.sending.set(false); } });
  }
  canResolve(): boolean { return ['OPEN', 'IN_PROGRESS', 'WAITING_LEARNER'].includes(this.request()?.status ?? ''); }
  resolve(): void {
    if (!this.canResolve() || this.resolving()) return;
    this.resolving.set(true); this.actionError.set(null); this.actionSuccess.set(null);
    this.data.resolve(this.requestId()).subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.actionError.set(issue); else { this.request.set(response.data); this.actionSuccess.set(`Yêu cầu được cập nhật: ${response.data.status}.`); } this.confirmResolve.set(false); this.resolving.set(false); }, error: (error: unknown) => { this.actionError.set(mentorApiErrorMessage(error)); this.resolving.set(false); this.confirmResolve.set(false); } });
  }
}
