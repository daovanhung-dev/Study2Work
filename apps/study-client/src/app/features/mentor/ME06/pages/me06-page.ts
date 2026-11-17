import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ME06ContentTreeService } from '../data-access/me06-content-tree.service';
import type { MentorContent } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [RouterLink, MentorPageHeader], selector: 'study-me06-page', styleUrls: ['./me06-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me06-page.html' })
export class ME06Page implements OnInit {
  private readonly data = inject(ME06ContentTreeService);
  private readonly route = inject(ActivatedRoute);
  readonly courseId = signal('');
  readonly content = signal<MentorContent[]>([]);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly invalidId = signal(false);
  ngOnInit(): void {
    const id = toSafeMentorId(this.route.snapshot.paramMap.get('courseId'));
    if (!id) { this.invalidId.set(true); this.loading.set(false); return; }
    this.courseId.set(id); this.load(id);
  }
  load(id = this.courseId()): void {
    if (!id) return;
    this.loading.set(true); this.error.set(null);
    this.data.list(id).subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.error.set(issue); else this.content.set(response.data); this.loading.set(false); }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.loading.set(false); } });
  }
  depth(row: MentorContent): number {
    let level = 0; let parentId = row.parent_id; const visited = new Set<string>();
    while (parentId != null && level < 8) { const id = String(parentId); if (visited.has(id)) return 0; visited.add(id); const parent = this.content().find((node) => String(node.id) === id); if (!parent) return 0; parentId = parent.parent_id; level++; }
    return level;
  }
  safeId(value: unknown): string | null { return toSafeMentorId(value); }
}
