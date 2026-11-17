import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { ME07ContentEditorService } from '../data-access/me07-content-editor.service';
import type { MentorContent } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [MentorPageHeader], selector: 'study-me07-page', styleUrls: ['./me07-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me07-page.html' })
export class ME07Page implements OnInit {
  private readonly data = inject(ME07ContentEditorService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  readonly courseId = signal('');
  readonly contentId = signal('');
  readonly content = signal<MentorContent | null>(null);
  readonly loading = signal(true);
  readonly saving = signal(false);
  readonly error = signal<string | null>(null);
  readonly success = signal<string | null>(null);
  readonly invalidRoute = signal(false);
  ngOnInit(): void {
    const courseId = toSafeMentorId(this.route.snapshot.paramMap.get('courseId'));
    if (!courseId) { this.invalidRoute.set(true); this.loading.set(false); return; }
    this.courseId.set(courseId);
    const contentId = toSafeMentorId(this.route.snapshot.paramMap.get('contentId'));
    this.contentId.set(contentId ?? '');
    this.load();
  }
  load(): void {
    this.loading.set(true); this.error.set(null);
    this.data.list(this.courseId()).subscribe({
      next: (response) => {
        const issue = mentorEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else if (this.contentId()) {
          const found = response.data.find((item) => toSafeMentorId(item.id) === this.contentId());
          if (found) this.content.set(found); else this.error.set('Không tìm thấy Content trong course này.');
        }
        this.loading.set(false);
      }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.loading.set(false); },
    });
  }
  save(event: SubmitEvent, title: string, contentType: string, payloadText: string): void {
    event.preventDefault();
    if (this.saving()) return;
    let payload: Record<string, unknown>;
    try {
      const parsed: unknown = JSON.parse(payloadText);
      if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) throw new Error('Payload cần là JSON object.');
      payload = parsed as Record<string, unknown>;
    } catch (error) {
      this.error.set(error instanceof Error ? error.message : 'Payload JSON không hợp lệ.');
      return;
    }
    this.error.set(null); this.success.set(null); this.saving.set(true);
    const body = { content_type: contentType, title, payload };
    const request = this.contentId()
      ? this.data.update(this.contentId(), body)
      : this.create(Number(this.courseId()), body);
    if (!request) { this.saving.set(false); this.error.set('Course ID vượt miền số an toàn của JSON client; không gửi mutation để tránh làm sai ID.'); return; }
    request.subscribe({
      next: (response) => {
        const issue = mentorEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else { this.success.set('Nội dung đã được lưu bởi Study Server.'); this.content.set(response.data); }
        this.saving.set(false);
      }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.saving.set(false); },
    });
  }
  private create(courseId: number, body: { content_type: string; title: string; payload: Record<string, unknown> }) {
    if (!Number.isSafeInteger(courseId) || courseId <= 0) return null;
    return this.data.create({ course_id: courseId, ...body });
  }
  backToTree(): void { void this.router.navigate(['/mentor/courses', this.courseId(), 'content']); }
  payloadValue(): string { return this.content() ? JSON.stringify(this.content()?.payload, null, 2) : '{}'; }
}
