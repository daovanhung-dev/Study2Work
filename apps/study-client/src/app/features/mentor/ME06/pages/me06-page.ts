import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import {
  EMPTY,
  Subject,
  catchError,
  distinctUntilChanged,
  map,
  of,
  startWith,
  switchMap,
  tap,
} from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ME06ContentTreeService } from '../data-access/me06-content-tree.service';
import type { MentorContent } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

type ContentLoadResult =
  | { courseId: string; response: ApiEnvelope<MentorContent[]> }
  | { courseId: string; error: unknown };

interface ContentTreeRow {
  node: MentorContent;
  depth: number;
}

@Component({
  imports: [RouterLink, MentorPageHeader],
  selector: 'study-me06-page',
  styleUrls: ['./me06-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me06-page.html',
})
export class ME06Page implements OnInit {
  private readonly data = inject(ME06ContentTreeService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly route = inject(ActivatedRoute);
  private readonly retry$ = new Subject<void>();

  readonly courseId = signal('');
  readonly content = signal<MentorContent[]>([]);
  readonly treeRows = computed(() => flattenContentTree(this.content()));
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly invalidId = signal(false);
  readonly notFound = signal(false);
  readonly forbidden = signal(false);

  ngOnInit(): void {
    this.route.paramMap
      .pipe(
        map((params) => toSafeMentorId(params.get('courseId'))),
        distinctUntilChanged(),
        tap((id) => this.resetForCourse(id)),
        switchMap((id) => {
          if (!id) return EMPTY;
          return this.retry$.pipe(
            startWith(undefined),
            tap(() => this.resetRequestState()),
            switchMap(() =>
              this.data.list(id).pipe(
                map((response): ContentLoadResult => ({ courseId: id, response })),
                catchError((error: unknown) => of<ContentLoadResult>({ courseId: id, error })),
              ),
            ),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyResult(result));
  }

  load(): void {
    if (this.courseId()) this.retry$.next();
  }

  safeId(value: unknown): string | null {
    return toSafeMentorId(value);
  }

  indent(depth: number): number {
    return Math.min(depth, 6) * 24;
  }

  private resetForCourse(id: string | null): void {
    this.courseId.set(id ?? '');
    this.content.set([]);
    this.error.set(null);
    this.notFound.set(false);
    this.forbidden.set(false);
    this.invalidId.set(id === null);
    this.loading.set(id !== null);
  }

  private resetRequestState(): void {
    this.content.set([]);
    this.error.set(null);
    this.notFound.set(false);
    this.forbidden.set(false);
    this.loading.set(true);
  }

  private applyResult(result: ContentLoadResult): void {
    if (this.courseId() !== result.courseId) return;
    this.loading.set(false);

    if ('error' in result) {
      this.notFound.set(hasHttpStatus(result.error, 404));
      this.forbidden.set(hasHttpStatus(result.error, 403));
      if (!this.notFound() && !this.forbidden()) {
        this.error.set(mentorApiErrorMessage(result.error));
      }
      return;
    }

    const envelope: unknown = result.response;
    if (!isApiEnvelope(envelope)) {
      this.error.set('Study Server trả về phản hồi không hợp lệ.');
      return;
    }
    if (!envelope.success) {
      this.notFound.set(envelope.businessCode === 'DESIGN_RESOURCE_NOT_FOUND');
      this.forbidden.set(envelope.businessCode === 'DESIGN_ACCESS_DENIED');
      if (!this.notFound() && !this.forbidden()) {
        this.error.set(envelope.message || 'Study Server không xác nhận yêu cầu.');
      }
      return;
    }
    if (
      envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isCourseContentList(envelope.data, result.courseId)
    ) {
      this.error.set('Study Server trả về cây nội dung không hợp lệ.');
      return;
    }

    this.content.set(envelope.data);
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isApiEnvelope(value: unknown): value is ApiEnvelope<unknown> {
  return (
    isRecord(value) &&
    typeof value['success'] === 'boolean' &&
    typeof value['businessCode'] === 'string' &&
    typeof value['message'] === 'string' &&
    isRecord(value['meta']) &&
    typeof value['traceId'] === 'string'
  );
}

function isCourseContentList(value: unknown, courseId: string): value is MentorContent[] {
  if (!Array.isArray(value)) return false;
  const ids = new Set<string>();
  const parents = new Map<string, string | null>();

  for (const item of value) {
    if (
      !isRecord(item) ||
      toSafeMentorId(item['id']) === null ||
      toSafeMentorId(item['course_id']) !== courseId ||
      typeof item['content_type'] !== 'string' ||
      typeof item['title'] !== 'string' ||
      !isRecord(item['payload']) ||
      typeof item['status'] !== 'string' ||
      !isInt32(item['order']) ||
      (item['parent_id'] !== undefined &&
        item['parent_id'] !== null &&
        toSafeMentorId(item['parent_id']) === null)
    ) {
      return false;
    }

    const id = toSafeMentorId(item['id']);
    if (!id || ids.has(id)) return false;
    ids.add(id);
    parents.set(id, item['parent_id'] == null ? null : toSafeMentorId(item['parent_id']));
  }

  for (const id of ids) {
    const visited = new Set([id]);
    let parentId = parents.get(id) ?? null;
    while (parentId !== null) {
      if (!ids.has(parentId) || visited.has(parentId)) return false;
      visited.add(parentId);
      parentId = parents.get(parentId) ?? null;
    }
  }
  return true;
}

function isInt32(value: unknown): value is number {
  return (
    Number.isInteger(value) &&
    Number(value) >= -(2 ** 31) &&
    Number(value) <= 2 ** 31 - 1
  );
}

function flattenContentTree(contents: MentorContent[]): ContentTreeRow[] {
  const children = new Map<string, MentorContent[]>();
  for (const node of contents) {
    const parentId = node.parent_id == null ? '' : toSafeMentorId(node.parent_id);
    if (parentId === null) continue;
    const siblings = children.get(parentId) ?? [];
    siblings.push(node);
    children.set(parentId, siblings);
  }

  const roots = children.get('') ?? [];
  const pending = roots
    .slice()
    .reverse()
    .map((node) => ({ node, depth: 0 }));
  const rows: ContentTreeRow[] = [];
  while (pending.length) {
    const current = pending.pop();
    if (!current) continue;
    rows.push(current);
    const nodeId = toSafeMentorId(current.node.id);
    if (!nodeId) continue;
    const nested = children.get(nodeId) ?? [];
    for (let index = nested.length - 1; index >= 0; index--) {
      const child = nested[index];
      if (child) pending.push({ node: child, depth: current.depth + 1 });
    }
  }
  return rows;
}

function hasHttpStatus(error: unknown, status: number): boolean {
  return isRecord(error) && error['status'] === status;
}
