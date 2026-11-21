import { DatePipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import {
  Subject,
  catchError,
  combineLatest,
  distinctUntilChanged,
  map,
  of,
  startWith,
  switchMap,
  tap,
} from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ST25ThreadService } from '../data-access/st25-thread.service';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import type {
  StudentAuthor,
  StudentDiscussion,
  StudentDiscussionComment,
  StudentPage,
} from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [DatePipe, FormsModule, RouterLink],
  selector: 'study-st25-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    '../../shared/ui/student-api-community.css',
    './st25-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st25-page.html',
})
export class ST25Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST25ThreadService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly retryThread$ = new Subject<void>();
  readonly discussionId = signal(toSafeStudyId(this.route.snapshot.paramMap.get('discussionId')));
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly replyError = signal<string | null>(null);
  readonly replyBusy = signal(false);
  readonly replySent = signal(false);
  readonly replyOutcomeUnknownDiscussionId = signal<string | null>(null);
  readonly failedAvatarIds = signal<ReadonlySet<string>>(new Set());
  readonly thread = signal<StudentDiscussion | null>(null);
  replyContent = '';

  ngOnInit(): void {
    const discussionId$ = this.route.paramMap.pipe(
      map((params) => toSafeStudyId(params.get('discussionId'))),
      distinctUntilChanged(),
      tap((discussionId) => {
        if (this.discussionId() === discussionId) return;
        this.discussionId.set(discussionId);
        this.replyContent = '';
        this.replyError.set(null);
        this.replySent.set(false);
        this.failedAvatarIds.set(new Set());
      }),
    );

    combineLatest([discussionId$, this.retryThread$.pipe(startWith(undefined))])
      .pipe(
        tap(() => {
          this.loading.set(true);
          this.error.set(null);
          this.thread.set(null);
        }),
        switchMap(([discussionId]) => this.loadThread(discussionId)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyThread(result));
  }

  retryThread(): void {
    this.retryThread$.next();
  }

  authorAvatarUrl(author: StudentAuthor): string | null {
    const id = toSafeStudyId(author.id);
    return id && !this.failedAvatarIds().has(id) ? safeAvatarUrl(author.avatar_url) : null;
  }

  authorInitials(author: StudentAuthor): string {
    const parts = author.full_name.trim().split(/\s+/).filter(Boolean);
    return parts.slice(-2).map((part) => Array.from(part)[0]?.toUpperCase() ?? '').join('') || '?';
  }

  markAvatarFailed(authorId: unknown): void {
    const id = toSafeStudyId(authorId);
    if (!id) return;
    this.failedAvatarIds.update((current) => new Set(current).add(id));
  }

  sendReply(): void {
    const discussionId = this.discussionId();
    const content = this.replyContent.trim();
    if (
      !discussionId ||
      !content ||
      this.replyBusy() ||
      this.replyOutcomeUnknownDiscussionId() === discussionId
    ) {
      if (!content) this.replyError.set('Nhập nội dung phản hồi.');
      return;
    }
    const existingCommentIds = new Set(
      this.thread()
        ?.comments.map((comment) => toSafeStudyId(comment.id))
        .filter((id): id is string => id !== null) ?? [],
    );
    this.replyBusy.set(true);
    this.replyError.set(null);
    this.replySent.set(false);
    this.data.reply(discussionId, content).subscribe({
      next: (response) => {
        if (!response.success) {
          if (this.discussionId() === discussionId) {
            this.replyError.set('Chưa thể gửi phản hồi. Vui lòng thử lại.');
          }
          this.replyBusy.set(false);
          return;
        }
        const updatedDiscussion = getUpdatedDiscussion(
          response.data,
          discussionId,
          content,
          existingCommentIds,
        );
        if (
          response.businessCode !== 'DESIGN_RESOURCE_CREATED' ||
          !updatedDiscussion
        ) {
          this.replyOutcomeUnknownDiscussionId.set(discussionId);
          if (this.discussionId() === discussionId) {
            this.replyError.set('Chưa thể xác nhận phản hồi đã được gửi. Nút gửi đã khóa để tránh tạo trùng.');
          }
          this.replyBusy.set(false);
          return;
        }
        this.replyBusy.set(false);
        if (this.destroyRef.destroyed || this.discussionId() !== discussionId) return;
        this.replyContent = '';
        this.replySent.set(true);
        this.thread.set(updatedDiscussion);
        this.retryThread$.next();
      },
      error: (error: unknown) => {
        if (error instanceof HttpErrorResponse && (error.status === 0 || error.status >= 500)) {
          this.replyOutcomeUnknownDiscussionId.set(discussionId);
        }
        if (this.discussionId() === discussionId) {
          this.replyError.set(studentApiErrorMessage(error));
        }
        this.replyBusy.set(false);
      },
    });
  }

  private loadThread(discussionId: string | null) {
    if (!discussionId) return of({ discussionId, response: null, error: null });
    return this.data.thread(discussionId).pipe(
      map((response) => ({ discussionId, response, error: null })),
      catchError((error: unknown) => of({ discussionId, response: null, error })),
    );
  }

  private applyThread(result: ThreadLoad): void {
    this.loading.set(false);
    if (!result.discussionId) {
      this.error.set('Không tìm thấy chủ đề này.');
      return;
    }
    if (result.error !== null) {
      this.error.set(studentApiErrorMessage(result.error));
      return;
    }
    const response = result.response;
    if (!response?.success) {
      this.error.set('Chưa thể tải chủ đề. Vui lòng thử lại.');
      return;
    }
    if (
      response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isThreadPage(response.data, result.discussionId)
    ) {
      this.error.set('Thông tin chủ đề không khớp. Hãy tải lại trang.');
      return;
    }
    this.thread.set(response.data.items[0]);
  }
}

interface ThreadLoad {
  discussionId: string | null;
  response: ApiEnvelope<StudentPage<StudentDiscussion>> | null;
  error: unknown | null;
}

function isThreadPage(value: unknown, discussionId: string): value is StudentPage<StudentDiscussion> {
  if (typeof value !== 'object' || value === null) return false;
  const page = value as Record<string, unknown>;
  const pagination = page['pagination'];
  if (
    !Array.isArray(page['items']) ||
    page['items'].length !== 1 ||
    typeof pagination !== 'object' ||
    pagination === null
  ) {
    return false;
  }
  const meta = pagination as Record<string, unknown>;
  const discussion = page['items'][0];
  return (
    isDiscussion(discussion) &&
    toSafeStudyId(discussion.id) === discussionId &&
    meta['page'] === 1 &&
    meta['size'] === 1 &&
    meta['total'] === 1 &&
    meta['total_pages'] === 1
  );
}

function getUpdatedDiscussion(
  value: unknown,
  discussionId: string,
  content: string,
  existingCommentIds: ReadonlySet<string>,
): StudentDiscussion | null {
  if (!isThreadPage(value, discussionId)) return null;
  const discussion = value.items[0];
  return discussion.comments.some(
    (comment) =>
      comment.content === content &&
      !existingCommentIds.has(toSafeStudyId(comment.id) ?? ''),
  )
    ? discussion
    : null;
}

function isDiscussion(value: unknown): value is StudentDiscussion {
  if (typeof value !== 'object' || value === null) return false;
  const discussion = value as Record<string, unknown>;
  return (
    toSafeStudyId(discussion['id']) !== null &&
    toSafeStudyId(discussion['course_id']) !== null &&
    typeof discussion['title'] === 'string' &&
    typeof discussion['content'] === 'string' &&
    discussion['status'] === 'ACTIVE' &&
    isAuthor(discussion['author']) &&
    Array.isArray(discussion['comments']) &&
    discussion['comments'].every((comment: unknown) =>
      isDiscussionComment(comment, toSafeStudyId(discussion['id']) ?? ''),
    )
  );
}

function isAuthor(value: unknown): boolean {
  if (typeof value !== 'object' || value === null) return false;
  const author = value as Record<string, unknown>;
  return (
    toSafeStudyId(author['id']) !== null &&
    typeof author['full_name'] === 'string' &&
    (author['avatar_url'] === undefined ||
      author['avatar_url'] === null ||
      typeof author['avatar_url'] === 'string')
  );
}

function isDiscussionComment(value: unknown, discussionId: string): value is StudentDiscussionComment {
  if (typeof value !== 'object' || value === null) return false;
  const comment = value as Record<string, unknown>;
  return (
    toSafeStudyId(comment['id']) !== null &&
    toSafeStudyId(comment['discussion_id']) === discussionId &&
    typeof comment['content'] === 'string' &&
    typeof comment['created_at'] === 'string' &&
    Number.isFinite(Date.parse(comment['created_at'])) &&
    isAuthor(comment['author'])
  );
}

function safeAvatarUrl(value: string | null): string | null {
  if (!value?.trim() || typeof globalThis.location === 'undefined') return null;
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
