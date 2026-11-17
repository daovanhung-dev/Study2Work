import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { ME08ContentActionsService } from '../data-access/me08-content-actions.service';
import type { MentorContent } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

type ContentAction = 'publish' | 'unpublish' | 'delete';

@Component({ imports: [RouterLink, MentorPageHeader], selector: 'study-me08-page', styleUrls: ['./me08-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me08-page.html' })
export class ME08Page implements OnInit {
  private readonly data = inject(ME08ContentActionsService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  readonly contentId = signal('');
  readonly courseId = signal('');
  readonly content = signal<MentorContent | null>(null);
  readonly allContent = signal<MentorContent[]>([]);
  readonly loading = signal(true);
  readonly working = signal(false);
  readonly error = signal<string | null>(null);
  readonly success = signal<string | null>(null);
  readonly pendingAction = signal<ContentAction | null>(null);
  readonly noCourseContext = signal(false);
  ngOnInit(): void {
    this.contentId.set(toSafeMentorId(this.route.snapshot.paramMap.get('contentId')) ?? '');
    const state = typeof history === 'undefined' ? {} : history.state as { courseId?: unknown };
    this.courseId.set(toSafeMentorId(state.courseId) ?? '');
    if (!this.contentId() || !this.courseId()) { this.noCourseContext.set(true); this.loading.set(false); return; }
    this.load();
  }
  load(): void {
    if (!this.courseId()) return;
    this.loading.set(true); this.error.set(null); this.pendingAction.set(null);
    this.data.content(this.courseId()).subscribe({
      next: (response) => {
        const issue = mentorEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else {
          this.allContent.set(response.data);
          this.content.set(response.data.find((item) => toSafeMentorId(item.id) === this.contentId()) ?? null);
          if (!this.content()) this.error.set('Không tìm thấy Content trong course context hiện tại.');
        }
        this.loading.set(false);
      }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.loading.set(false); },
    });
  }
  hasChildren(): boolean { return this.allContent().some((item) => String(item.parent_id ?? '') === this.contentId()); }
  canChangePublication(): boolean { return ['APPROVED', 'PUBLISHED'].includes(this.content()?.status ?? ''); }
  canDelete(): boolean { return !!this.content() && this.content()?.status !== 'PUBLISHED' && !this.hasChildren(); }
  ask(action: ContentAction): void { this.pendingAction.set(action); this.error.set(null); }
  cancel(): void { this.pendingAction.set(null); }
  confirm(): void {
    const action = this.pendingAction(); const item = this.content();
    if (!action || !item || this.working()) return;
    this.working.set(true); this.error.set(null); this.success.set(null);
    if (action === 'delete') {
      this.data.delete(this.contentId()).subscribe({
        next: (response) => {
          const issue = mentorEnvelopeError(response.success, response.message);
          if (issue) { this.error.set(issue); this.working.set(false); return; }
          this.success.set('Nội dung đã được gỡ theo phản hồi của Study Server.');
          this.pendingAction.set(null); this.working.set(false);
          void this.router.navigate(['/mentor/courses', this.courseId(), 'content']);
        }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.working.set(false); },
      });
      return;
    }
    const published = action === 'publish';
    this.data.publish(this.contentId(), published).subscribe({
      next: (response) => {
        const issue = mentorEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else { this.content.set(response.data); this.success.set(`Trạng thái nội dung: ${response.data.status}.`); }
        this.pendingAction.set(null); this.working.set(false);
      }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.working.set(false); },
    });
  }
  actionTitle(): string {
    switch (this.pendingAction()) {
      case 'publish': return 'Xuất bản nội dung?';
      case 'unpublish': return 'Đưa nội dung về APPROVED?';
      case 'delete': return 'Gỡ nội dung này?';
      default: return '';
    }
  }
}
