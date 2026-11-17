import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ME15NotificationStatusService } from '../data-access/me15-notification-status.service';
import type { MentorNotificationOperation } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [DatePipe, RouterLink, MentorPageHeader], selector: 'study-me15-page', styleUrls: ['./me15-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me15-page.html' })
export class ME15Page implements OnInit {
  private readonly data = inject(ME15NotificationStatusService);
  private readonly route = inject(ActivatedRoute);
  readonly notificationId = signal('');
  readonly operation = signal<MentorNotificationOperation | null>(null);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly invalidId = signal(false);
  ngOnInit(): void {
    const id = toSafeMentorId(this.route.snapshot.paramMap.get('notificationId'));
    if (!id) { this.invalidId.set(true); this.loading.set(false); return; }
    this.notificationId.set(id); this.load(id);
  }
  load(id = this.notificationId()): void {
    if (!id) return;
    this.loading.set(true); this.error.set(null);
    this.data.status(id).subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.error.set(issue); else this.operation.set(response.data); this.loading.set(false); }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.loading.set(false); } });
  }
}
