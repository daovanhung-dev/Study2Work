import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { StudentApiService, type DiscussionRecord, type StudentPage } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st25-page',
  styleUrls: ['./st25-page.css', './st25-visual.css', '../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st25-page.html',
})
export class ST25Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(StudentApiService);
  readonly thread = new StudentApiState<StudentPage<DiscussionRecord>>();
  readonly reply = new StudentApiState<DiscussionRecord>();
  discussionId = '';
  replyText = '';

  ngOnInit(): void {
    this.discussionId = this.route.snapshot.paramMap.get('discussionId') ?? '';
    this.reloadThread();
  }

  reloadThread(): void {
    if (this.discussionId) this.thread.load(this.api.getDiscussion(this.discussionId));
  }

  submitReply(): void {
    if (!this.discussionId || !this.replyText.trim() || this.reply.status() === 'loading') return;
    this.reply.load(this.api.addDiscussionComment(this.discussionId, this.replyText.trim()), () => {
      this.replyText = '';
      this.reloadThread();
    });
  }
}
