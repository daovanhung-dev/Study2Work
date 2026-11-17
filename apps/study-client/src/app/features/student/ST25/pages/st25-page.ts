import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ST25ThreadService } from '../data-access/st25-thread.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentDiscussion } from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [DatePipe, FormsModule, RouterLink],
  selector: 'study-st25-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    '../../shared/ui/student-api-community.css',
    './st25-page.css',
    './st25-visual.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st25-page.html',
})
export class ST25Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST25ThreadService);
  private readonly discussionId = toSafeStudyId(this.route.snapshot.paramMap.get('discussionId'));
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly replyError = signal<string | null>(null);
  readonly replyBusy = signal(false);
  readonly replySent = signal(false);
  readonly thread = signal<StudentDiscussion | null>(null);
  replyContent = '';

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    if (!this.discussionId) {
      this.error.set('Mã thảo luận không hợp lệ.');
      this.loading.set(false);
      return;
    }
    this.loading.set(true);
    this.error.set(null);
    this.data.thread(this.discussionId).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else
          this.thread.set(
            response.data.items.find((item) => String(item.id) === this.discussionId) ??
              response.data.items[0] ??
              null,
          );
        this.loading.set(false);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.loading.set(false);
      },
    });
  }

  sendReply(): void {
    const content = this.replyContent.trim();
    if (!this.discussionId || !content || this.replyBusy()) {
      this.replyError.set(content ? null : 'Nhập nội dung phản hồi.');
      return;
    }
    this.replyBusy.set(true);
    this.replyError.set(null);
    this.replySent.set(false);
    this.data.reply(this.discussionId, content).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) {
          this.replyError.set(issue);
          this.replyBusy.set(false);
          return;
        }
        this.replyContent = '';
        this.replySent.set(true);
        this.replyBusy.set(false);
        this.load();
      },
      error: (error: unknown) => {
        this.replyError.set(studentApiErrorMessage(error));
        this.replyBusy.set(false);
      },
    });
  }
}
