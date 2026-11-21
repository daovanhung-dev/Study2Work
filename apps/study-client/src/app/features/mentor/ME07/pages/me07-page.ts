import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
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

import { ME07ContentEditorService } from '../data-access/me07-content-editor.service';
import type { MentorContent } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

type ME07RouteState = {
  courseId: string | null;
  contentId: string | null;
  invalid: boolean;
};

type ME07LoadResult =
  | { courseId: string; contentId: string | null; response: ApiEnvelope<MentorContent[]> }
  | { courseId: string; contentId: string | null; error: unknown };

@Component({
  imports: [RouterLink, MentorPageHeader],
  selector: 'study-me07-page',
  styleUrls: ['./me07-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me07-page.html',
})
export class ME07Page implements OnInit {
  private readonly data = inject(ME07ContentEditorService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly retry$ = new Subject<void>();

  readonly courseId = signal('');
  readonly contentId = signal('');
  readonly content = signal<MentorContent | null>(null);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly invalidRoute = signal(false);
  readonly notFound = signal(false);
  readonly forbidden = signal(false);

  ngOnInit(): void {
    this.route.paramMap
      .pipe(
        map((params): ME07RouteState => {
          const courseId = toSafeMentorId(params.get('courseId'));
          const rawContentId = params.get('contentId');
          const contentId = rawContentId === null ? null : toSafeMentorId(rawContentId);
          return {
            courseId,
            contentId,
            invalid: courseId === null || (rawContentId !== null && contentId === null),
          };
        }),
        distinctUntilChanged(
          (previous, current) =>
            previous.courseId === current.courseId &&
            previous.contentId === current.contentId &&
            previous.invalid === current.invalid,
        ),
        tap((state) => this.resetForRoute(state)),
        switchMap((state) => {
          const courseId = state.courseId;
          if (state.invalid || courseId === null) return EMPTY;
          return this.retry$.pipe(
            startWith(undefined),
            tap(() => this.resetRequestState()),
            switchMap(() =>
              this.data.list(courseId).pipe(
                map(
                  (response): ME07LoadResult => ({
                    courseId,
                    contentId: state.contentId,
                    response,
                  }),
                ),
                catchError((error: unknown) =>
                  of<ME07LoadResult>({
                    courseId,
                    contentId: state.contentId,
                    error,
                  }),
                ),
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

  save(event: SubmitEvent): void {
    event.preventDefault();
    this.error.set('Lưu nội dung đang bị khóa cho tới khi schema payload và request #51 được duyệt.');
  }

  backToTree(): void {
    if (!this.courseId()) return;
    void this.router.navigate(['/mentor/courses', this.courseId(), 'content']);
  }

  private resetForRoute(state: ME07RouteState): void {
    this.courseId.set(state.courseId ?? '');
    this.contentId.set(state.contentId ?? '');
    this.content.set(null);
    this.error.set(null);
    this.notFound.set(false);
    this.forbidden.set(false);
    this.invalidRoute.set(state.invalid);
    this.loading.set(!state.invalid);
  }

  private resetRequestState(): void {
    this.content.set(null);
    this.error.set(null);
    this.notFound.set(false);
    this.forbidden.set(false);
    this.loading.set(true);
  }

  private applyResult(result: ME07LoadResult): void {
    if (this.courseId() !== result.courseId || this.contentId() !== (result.contentId ?? '')) return;
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
      !isContentList(envelope.data, result.courseId)
    ) {
      this.error.set('Study Server trả về danh sách Content không hợp lệ.');
      return;
    }

    if (result.contentId) {
      const selected = envelope.data.find((item) => toSafeMentorId(item.id) === result.contentId);
      if (!selected) {
        this.notFound.set(true);
        return;
      }
      this.content.set(selected);
    }
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
  const ids = new Set<string>();
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
  }
  return true;
}

function isInt32(value: unknown): value is number {
  return Number.isInteger(value) && Number(value) >= -(2 ** 31) && Number(value) <= 2 ** 31 - 1;
}

function hasHttpStatus(error: unknown, status: number): boolean {
  return isRecord(error) && error['status'] === status;
}
