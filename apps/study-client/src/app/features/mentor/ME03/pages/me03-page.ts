import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ME03WorkspaceService } from '../data-access/me03-workspace.service';
import type { MentorContent, MentorCourse, MentorCourseProgressRow } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [RouterLink, MentorPageHeader], selector: 'study-me03-page', styleUrls: ['./me03-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me03-page.html' })
export class ME03Page implements OnInit {
  private readonly data = inject(ME03WorkspaceService);
  private readonly route = inject(ActivatedRoute);
  readonly courseId = signal('');
  readonly courseTitle = signal('Workspace khóa học');
  readonly content = signal<MentorContent[]>([]);
  readonly progress = signal<MentorCourseProgressRow[]>([]);
  readonly loadingContent = signal(true);
  readonly loadingProgress = signal(true);
  readonly contentError = signal<string | null>(null);
  readonly progressError = signal<string | null>(null);
  readonly invalidId = signal(false);
  ngOnInit(): void {
    const id = toSafeMentorId(this.route.snapshot.paramMap.get('courseId'));
    if (!id) { this.invalidId.set(true); this.loadingContent.set(false); this.loadingProgress.set(false); return; }
    this.courseId.set(id); this.load();
  }
  load(): void {
    const id = this.courseId(); if (!id) return;
    this.loadingContent.set(true); this.loadingProgress.set(true); this.contentError.set(null); this.progressError.set(null);
    this.data.courses().subscribe({ next: (response) => { if (response.success) this.courseTitle.set(response.data.items.find((course: MentorCourse) => toSafeMentorId(course.id) === id)?.title ?? 'Workspace khóa học'); }, error: () => undefined });
    this.data.content(id).subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.contentError.set(issue); else this.content.set(response.data); this.loadingContent.set(false); }, error: (error: unknown) => { this.contentError.set(mentorApiErrorMessage(error)); this.loadingContent.set(false); } });
    this.data.progress(id).subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.progressError.set(issue); else this.progress.set(response.data.items); this.loadingProgress.set(false); }, error: (error: unknown) => { this.progressError.set(mentorApiErrorMessage(error)); this.loadingProgress.set(false); } });
  }
  safeId(value: unknown): string | null { return toSafeMentorId(value); }
  depth(row: MentorContent): number {
    let depth = 0; let parentId = row.parent_id; const seen = new Set<string>();
    while (parentId != null && depth < 8) { const key = String(parentId); if (seen.has(key)) break; seen.add(key); const parent = this.content().find((candidate) => String(candidate.id) === key); if (!parent) break; parentId = parent.parent_id; depth++; }
    return depth;
  }
}
