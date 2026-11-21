import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import {
  EMPTY,
  Observable,
  catchError,
  distinctUntilChanged,
  map,
  merge,
  of,
  Subject,
  shareReplay,
  switchMap,
  tap,
  withLatestFrom,
} from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { MentorSessionError } from '../../../../core/auth/mentor-session.service';
import { ME03WorkspaceService } from '../data-access/me03-workspace.service';
import type {
  MentorContent,
  MentorCourse,
  MentorCourseProgressRow,
  MentorPage,
  MentorStudentSummary,
} from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({
  imports: [RouterLink, MentorPageHeader],
  selector: 'study-me03-page',
  styleUrls: ['./me03-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me03-page.html',
})
export class ME03Page implements OnInit {
  private readonly data = inject(ME03WorkspaceService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly route = inject(ActivatedRoute);
  private readonly refresh$ = new Subject<void>();

  readonly courseId = signal('');
  readonly courseTitle = signal('Workspace khóa học');
  readonly content = signal<MentorContent[]>([]);
  readonly progress = signal<MentorCourseProgressRow[]>([]);
  readonly failedStudentAvatarIds = signal<ReadonlySet<string>>(new Set());
  readonly loadingContent = signal(true);
  readonly loadingProgress = signal(true);
  readonly accessError = signal<string | null>(null);
  readonly contentError = signal<string | null>(null);
  readonly progressError = signal<string | null>(null);
  readonly invalidId = signal(false);

  ngOnInit(): void {
    const courseId$ = this.route.paramMap
      .pipe(
        map((params) => toSafeMentorId(params.get('courseId'))),
        distinctUntilChanged(),
        tap((id) => this.resetForCourse(id)),
        shareReplay({ bufferSize: 1, refCount: true }),
      );
    const courseTitleEvents$ = courseId$.pipe(
      switchMap((id) => {
        if (!id) return EMPTY;
        return capture(this.data.courses()).pipe(
          map((result): ME03LoadEvent => ({ id, kind: 'courses', result })),
        );
      }),
    );
    const routeLoads$ = courseId$.pipe(map((id) => ({ id, refresh: false })));
    const refreshLoads$ = this.refresh$.pipe(
      withLatestFrom(courseId$),
      map(([, id]) => ({ id, refresh: true })),
    );
    const workspaceEvents$ = merge(routeLoads$, refreshLoads$)
      .pipe(
        tap(({ id, refresh }) => {
          if (refresh && id) this.resetForRefresh();
        }),
        switchMap(({ id, refresh }) => {
          if (!id) return EMPTY;
          return merge(
            capture(this.data.content(id)).pipe(
              map((result): ME03LoadEvent => ({ id, kind: 'content', result })),
            ),
            capture(this.data.progress(id)).pipe(
              map((result): ME03LoadEvent => ({ id, kind: 'progress', result })),
            ),
          );
        }),
      );

    merge(courseTitleEvents$, workspaceEvents$)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((event) => {
        if (this.courseId() !== event.id) return;
        switch (event.kind) {
          case 'courses':
            this.applyCourseTitle(event.result, event.id);
            break;
          case 'content':
            this.applyContent(event.result, event.id);
            break;
          case 'progress':
            this.applyProgress(event.result);
            break;
        }
      });
  }

  safeId(value: unknown): string | null {
    return toSafeMentorId(value);
  }

  studentAvatarUrl(student: MentorStudentSummary): string | null {
    const id = toSafeMentorId(student.id);
    return id && !this.failedStudentAvatarIds().has(id)
      ? safeMentorAvatarUrl(student.avatar_url)
      : null;
  }

  studentInitials(student: MentorStudentSummary): string {
    const parts = student.full_name.trim().split(/\s+/).filter(Boolean);
    return parts.slice(-2).map((part) => Array.from(part)[0]?.toUpperCase() ?? '').join('') || '?';
  }

  markStudentAvatarFailed(studentId: unknown): void {
    const id = toSafeMentorId(studentId);
    if (!id) return;
    this.failedStudentAvatarIds.update((current) => new Set(current).add(id));
  }

  refreshWorkspace(): void {
    if (
      !this.courseId() ||
      this.invalidId() ||
      this.accessError() ||
      this.loadingContent() ||
      this.loadingProgress()
    ) {
      return;
    }
    this.refresh$.next();
  }

  depth(row: MentorContent): number {
    let depth = 0;
    let parentId = row.parent_id;
    const seen = new Set<string>();
    while (parentId != null && depth < 8) {
      const key = toSafeMentorId(parentId);
      if (!key || seen.has(key)) break;
      seen.add(key);
      const parent = this.content().find((candidate) => toSafeMentorId(candidate.id) === key);
      if (!parent) break;
      parentId = parent.parent_id;
      depth++;
    }
    return depth;
  }

  private resetForCourse(id: string | null): void {
    this.courseId.set(id ?? '');
    this.courseTitle.set(id ? `Workspace khóa học #${id}` : 'Workspace khóa học');
    this.content.set([]);
    this.progress.set([]);
    this.failedStudentAvatarIds.set(new Set());
    this.accessError.set(null);
    this.invalidId.set(id === null);
    this.loadingContent.set(id !== null);
    this.loadingProgress.set(id !== null);
    this.contentError.set(null);
    this.progressError.set(null);
  }

  private resetForRefresh(): void {
    this.content.set([]);
    this.progress.set([]);
    this.loadingContent.set(true);
    this.loadingProgress.set(true);
    this.contentError.set(null);
    this.progressError.set(null);
  }

  private applyCourseTitle(result: RequestResult<MentorPage<MentorCourse>>, id: string): void {
    if (this.accessError()) return;
    if (!result.ok) {
      this.failClosedForAccessError(result.error);
      return;
    }
    const response = result.response;
    if (
      !response?.success ||
      response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isMentorPage(response.data, 1, 20) ||
      !response.data.items.every(isCourseSummary)
    ) {
      return;
    }
    const course = response.data.items.find((item) => toSafeMentorId(item.id) === id);
    if (course) this.courseTitle.set(course.title);
  }

  private applyContent(result: RequestResult<MentorContent[]>, id: string): void {
    if (this.accessError()) return;
    this.loadingContent.set(false);
    if (!result.ok) {
      if (this.failClosedForAccessError(result.error)) return;
      this.contentError.set(mentorApiErrorMessage(result.error));
      return;
    }
    const response = result.response;
    if (
      !response?.success ||
      response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isCourseContentList(response.data, id)
    ) {
      this.contentError.set(response?.message || 'Study Server trả về cây nội dung không hợp lệ.');
      return;
    }
    this.content.set(response.data);
  }

  private applyProgress(result: RequestResult<MentorPage<MentorCourseProgressRow>>): void {
    if (this.accessError()) return;
    this.loadingProgress.set(false);
    if (!result.ok) {
      if (this.failClosedForAccessError(result.error)) return;
      this.progressError.set(mentorApiErrorMessage(result.error));
      return;
    }
    const response = result.response;
    if (
      !response?.success ||
      response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isProgressPage(response.data)
    ) {
      this.progressError.set(response?.message || 'Study Server trả về tiến độ không hợp lệ.');
      return;
    }
    this.progress.set(response.data.items);
  }

  private failClosedForAccessError(error: unknown): boolean {
    if (!isWorkspaceAccessError(error)) return false;
    this.accessError.set(mentorApiErrorMessage(error));
    this.courseTitle.set('Workspace khóa học');
    this.content.set([]);
    this.progress.set([]);
    this.loadingContent.set(false);
    this.loadingProgress.set(false);
    this.contentError.set(null);
    this.progressError.set(null);
    return true;
  }
}

type RequestResult<T> =
  | { ok: true; response: ApiEnvelope<T> }
  | { ok: false; error: unknown };

type ME03LoadEvent =
  | { id: string; kind: 'courses'; result: RequestResult<MentorPage<MentorCourse>> }
  | { id: string; kind: 'content'; result: RequestResult<MentorContent[]> }
  | {
      id: string;
      kind: 'progress';
      result: RequestResult<MentorPage<MentorCourseProgressRow>>;
    };

function capture<T>(request: Observable<ApiEnvelope<T>>): Observable<RequestResult<T>> {
  return request.pipe(
    map((response): RequestResult<T> => ({ ok: true, response })),
    catchError((error: unknown) => of<RequestResult<T>>({ ok: false, error })),
  );
}

function isWorkspaceAccessError(error: unknown): boolean {
  return error instanceof MentorSessionError ||
    (error instanceof HttpErrorResponse && [401, 403, 404].includes(error.status));
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isMentorPage<T>(
  value: unknown,
  expectedPage: number,
  expectedSize: number,
): value is MentorPage<T> {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) {
    return false;
  }
  const pagination = value['pagination'];
  const total = pagination['total'];
  return (
    pagination['page'] === expectedPage &&
    pagination['size'] === expectedSize &&
    value['items'].length <= expectedSize &&
    Number.isSafeInteger(total) &&
    Number(total) >= value['items'].length &&
    pagination['total_pages'] ===
      (Number(total) > 0 ? Math.ceil(Number(total) / expectedSize) : 0)
  );
}

function isCourseSummary(value: unknown): value is MentorCourse {
  return (
    isRecord(value) &&
    toSafeMentorId(value['id']) !== null &&
    typeof value['title'] === 'string' &&
    typeof value['status'] === 'string'
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
      !Number.isSafeInteger(item['order']) ||
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

function isProgressPage(value: unknown): value is MentorPage<MentorCourseProgressRow> {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) {
    return false;
  }
  const pagination = value['pagination'];
  const total = pagination['total'];
  const size = pagination['size'];
  if (
    pagination['page'] !== 1 ||
    !Number.isSafeInteger(total) ||
    Number(total) !== value['items'].length ||
    !Number.isSafeInteger(size) ||
    Number(size) !== value['items'].length ||
    pagination['total_pages'] !== (value['items'].length > 0 ? 1 : 0)
  ) {
    return false;
  }
  return value['items'].every((item: unknown) => {
    if (!isRecord(item) || !isRecord(item['student'])) return false;
    const student = item['student'];
    return (
      toSafeMentorId(student['id']) !== null &&
      typeof student['full_name'] === 'string' &&
      (student['avatar_url'] === undefined ||
        student['avatar_url'] === null ||
        typeof student['avatar_url'] === 'string') &&
      Number.isSafeInteger(item['completed_lessons']) &&
      Number(item['completed_lessons']) >= 0 &&
      Number.isSafeInteger(item['total_lessons']) &&
      Number(item['total_lessons']) >= Number(item['completed_lessons']) &&
      Number.isSafeInteger(item['progress_percent']) &&
      Number(item['progress_percent']) >= 0 &&
      Number(item['progress_percent']) <= 100
    );
  });
}

function safeMentorAvatarUrl(value: unknown): string | null {
  if (typeof value !== 'string' || !value.trim() || typeof globalThis.location === 'undefined') {
    return null;
  }
  try {
    const origin = globalThis.location.origin;
    const url = new URL(value, origin);
    return url.protocol === 'https:' || (url.protocol === 'http:' && url.origin === origin)
      ? url.href
      : null;
  } catch {
    return null;
  }
}
