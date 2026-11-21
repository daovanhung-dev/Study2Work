import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
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

import { ME08ContentActionsService } from '../data-access/me08-content-actions.service';
import type { MentorContent } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

type ME08RouteState = {
  contentId: string | null;
  courseId: string | null;
  invalid: boolean;
};

type ME08LoadResult =
  | { contentId: string; courseId: string; response: ApiEnvelope<MentorContent[]> }
  | { contentId: string; courseId: string; error: unknown };

@Component({
  imports: [RouterLink, MentorPageHeader],
  selector: 'study-me08-page',
  styleUrls: ['./me08-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me08-page.html',
})
export class ME08Page implements OnInit {
  private readonly data = inject(ME08ContentActionsService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly route = inject(ActivatedRoute);
  private readonly retry$ = new Subject<void>();

  readonly contentId = signal('');
  readonly courseId = signal('');
  readonly content = signal<MentorContent | null>(null);
  readonly allContent = signal<MentorContent[]>([]);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly invalidRoute = signal(false);
  readonly notFound = signal(false);
  readonly forbidden = signal(false);

  ngOnInit(): void {
    this.route.paramMap
      .pipe(
        map((params): ME08RouteState => {
          const contentId = toSafeMentorId(params.get('contentId'));
          const historyState: unknown = typeof history === 'undefined' ? null : history.state;
          const courseId = isRecord(historyState) ? toSafeMentorId(historyState['courseId']) : null;
          return { contentId, courseId, invalid: contentId === null || courseId === null };
        }),
        distinctUntilChanged(
          (previous, current) =>
            previous.contentId === current.contentId &&
            previous.courseId === current.courseId &&
            previous.invalid === current.invalid,
        ),
        tap((state) => this.resetForRoute(state)),
        switchMap((state) => {
          const { contentId, courseId } = state;
          if (state.invalid || contentId === null || courseId === null) return EMPTY;
          return this.retry$.pipe(
            startWith(undefined),
            tap(() => this.resetRequestState()),
            switchMap(() =>
              this.data.content(courseId).pipe(
                map((response): ME08LoadResult => ({ contentId, courseId, response })),
                catchError((error: unknown) => of<ME08LoadResult>({ contentId, courseId, error })),
              ),
            ),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyResult(result));
  }

  load(): void {
    if (this.contentId() && this.courseId()) this.retry$.next();
  }

  hasChildren(): boolean {
    const contentId = this.contentId();
    return this.allContent().some((item) => toSafeMentorId(item.parent_id) === contentId);
  }

  private resetForRoute(state: ME08RouteState): void {
    this.contentId.set(state.contentId ?? '');
    this.courseId.set(state.courseId ?? '');
    this.content.set(null);
    this.allContent.set([]);
    this.error.set(null);
    this.notFound.set(false);
    this.forbidden.set(false);
    this.invalidRoute.set(state.invalid);
    this.loading.set(!state.invalid);
  }

  private resetRequestState(): void {
    this.content.set(null);
    this.allContent.set([]);
    this.error.set(null);
    this.notFound.set(false);
    this.forbidden.set(false);
    this.loading.set(true);
  }

  private applyResult(result: ME08LoadResult): void {
    if (this.contentId() !== result.contentId || this.courseId() !== result.courseId) return;
    this.loading.set(false);

    if ('error' in result) {
      this.notFound.set(hasHttpStatus(result.error, 404));
      this.forbidden.set(hasHttpStatus(result.error, 403));
      if (!this.notFound() && !this.forbidden()) this.error.set(mentorApiErrorMessage(result.error));
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
      !isContentList(envelope.data, result.courseId)
    ) {
      this.error.set('Study Server trả về danh sách Content không hợp lệ.');
      return;
    }

    this.allContent.set(envelope.data);
    const selected = envelope.data.find((item) => toSafeMentorId(item.id) === result.contentId);
    if (!selected) {
      this.notFound.set(true);
      return;
    }
    this.content.set(selected);
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

function isContentList(value: unknown, courseId: string): value is MentorContent[] {
  if (!Array.isArray(value)) return false;
  const items = new Map<string, Record<string, unknown>>();
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
      (item['parent_id'] !== undefined && item['parent_id'] !== null && toSafeMentorId(item['parent_id']) === null)
    ) {
      return false;
    }
    const id = toSafeMentorId(item['id']);
    if (id === null || items.has(id)) return false;
    items.set(id, item);
  }

  for (const [id, item] of items) {
    const parentId = item['parent_id'] == null ? null : toSafeMentorId(item['parent_id']);
    if (parentId !== null && (!items.has(parentId) || parentId === id)) return false;
    const visited = new Set<string>([id]);
    let currentParent = parentId;
    while (currentParent !== null) {
      if (visited.has(currentParent)) return false;
      visited.add(currentParent);
      const parent = items.get(currentParent);
      currentParent = parent?.['parent_id'] == null ? null : toSafeMentorId(parent['parent_id']);
      if (parent && currentParent === null && parent['parent_id'] != null) return false;
    }
  }
  return true;
}

function isInt32(value: unknown): value is number {
  return Number.isInteger(value) && Number(value) >= -(2 ** 31) && Number(value) <= 2 ** 31 - 1;
}

function hasHttpStatus(error: unknown, status: number): boolean {
  return isRecord(error) && error['status'] === status;
}
