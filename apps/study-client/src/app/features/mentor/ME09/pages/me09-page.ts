import { DatePipe } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import {
  Subject,
  catchError,
  map,
  of,
  switchMap,
  tap,
} from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ME09SubmissionsService } from '../data-access/me09-submissions.service';
import type { MentorPage, MentorSubmission } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

type ME09Query = { page: number; courseId: string; status: string };
type ME09Result =
  | { query: ME09Query; response: ApiEnvelope<MentorPage<MentorSubmission>> }
  | { query: ME09Query; error: unknown };

@Component({
  imports: [DatePipe, RouterLink, MentorPageHeader],
  selector: 'study-me09-page',
  styleUrls: ['./me09-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me09-page.html',
})
export class ME09Page implements OnInit {
  private readonly data = inject(ME09SubmissionsService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly query$ = new Subject<ME09Query>();

  readonly submissions = signal<MentorSubmission[]>([]);
  readonly page = signal(1);
  readonly total = signal(0);
  readonly totalPages = signal(0);
  readonly courseFilter = signal('');
  readonly statusFilter = signal('');
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);

  ngOnInit(): void {
    this.query$
      .pipe(
        tap((query) => this.resetForQuery(query)),
        switchMap((query) =>
          this.data.list(query.page, query.courseId, query.status).pipe(
            map((response): ME09Result => ({ query, response })),
            catchError((error: unknown) => of<ME09Result>({ query, error })),
          ),
        ),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyResult(result));
    this.load();
  }

  load(page = this.page(), courseId = this.courseFilter(), status = this.statusFilter()): void {
    const normalizedCourseId = courseId.trim();
    const normalizedStatus = status.trim();
    if (!Number.isInteger(page) || page < 1 || page > 2 ** 31 - 1) {
      this.loading.set(false);
      this.error.set('Số trang cần là số nguyên dương trong giới hạn API.');
      return;
    }
    if (normalizedCourseId && !toSafeMentorId(normalizedCourseId)) {
      this.loading.set(false);
      this.error.set('Course ID cần là số nguyên dương int64.');
      return;
    }
    this.query$.next({ page, courseId: normalizedCourseId, status: normalizedStatus });
  }

  applyFilters(courseId: string, status: string): void {
    this.load(1, courseId, status);
  }

  safeId(value: unknown): string | null {
    return toSafeMentorId(value);
  }

  private resetForQuery(query: ME09Query): void {
    this.page.set(query.page);
    this.courseFilter.set(query.courseId);
    this.statusFilter.set(query.status);
    this.submissions.set([]);
    this.total.set(0);
    this.totalPages.set(0);
    this.loading.set(true);
    this.error.set(null);
  }

  private applyResult(result: ME09Result): void {
    if (!this.isCurrentQuery(result.query)) return;
    this.loading.set(false);

    if ('error' in result) {
      this.error.set(mentorApiErrorMessage(result.error));
      return;
    }

    const envelope: unknown = result.response;
    if (!isApiEnvelope(envelope)) {
      this.error.set('Study Server trả về phản hồi không hợp lệ.');
      return;
    }
    if (!envelope.success) {
      this.error.set(envelope.message || 'Study Server không xác nhận yêu cầu.');
      return;
    }
    if (
      envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isSubmissionPage(envelope.data, result.query.page)
    ) {
      this.error.set('Study Server trả về danh sách bài nộp không hợp lệ.');
      return;
    }

    this.submissions.set(envelope.data.items);
    this.page.set(envelope.data.pagination.page);
    this.total.set(envelope.data.pagination.total);
    this.totalPages.set(envelope.data.pagination.total_pages);
  }

  private isCurrentQuery(query: ME09Query): boolean {
    return (
      this.page() === query.page &&
      this.courseFilter() === query.courseId &&
      this.statusFilter() === query.status
    );
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

function isSubmissionPage(value: unknown, requestedPage: number): value is MentorPage<MentorSubmission> {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) return false;
  const pagination = value['pagination'];
  const { page, size, total, total_pages: totalPages } = pagination;
  if (
    !isNonNegativeInt(page) || page !== requestedPage ||
    !isNonNegativeInt(size) || size !== 20 ||
    !isNonNegativeInt(total) ||
    !isNonNegativeInt(totalPages) ||
    totalPages !== Math.ceil(total / size) ||
    value['items'].length > size
  ) {
    return false;
  }
  const ids = new Set<string>();
  for (const item of value['items']) {
    if (!isSubmission(item)) return false;
    const id = toSafeMentorId(item['id']);
    if (id === null || ids.has(id)) return false;
    ids.add(id);
  }
  return true;
}

function isSubmission(value: unknown): value is MentorSubmission {
  if (
    !isRecord(value) ||
    toSafeMentorId(value['id']) === null ||
    toSafeMentorId(value['assignment_id']) === null ||
    toSafeMentorId(value['user_id']) === null ||
    typeof value['status'] !== 'string' ||
    typeof value['submitted_at'] !== 'string' ||
    Number.isNaN(Date.parse(value['submitted_at'])) ||
    !Array.isArray(value['files'])
  ) {
    return false;
  }
  if (value['content'] !== undefined && value['content'] !== null && typeof value['content'] !== 'string') return false;
  if (value['score'] !== undefined && value['score'] !== null && typeof value['score'] !== 'string') return false;
  if (value['feedback'] !== undefined && value['feedback'] !== null && typeof value['feedback'] !== 'string') return false;
  return value['files'].every(isUploadAsset);
}

function isUploadAsset(value: unknown): boolean {
  return (
    isRecord(value) &&
    toSafeMentorId(value['id']) !== null &&
    typeof value['name'] === 'string' &&
    typeof value['url'] === 'string' &&
    typeof value['content_type'] === 'string' &&
    Number.isSafeInteger(value['size_bytes']) && Number(value['size_bytes']) >= 0 &&
    typeof value['status'] === 'string'
  );
}

function isNonNegativeInt(value: unknown): value is number {
  return Number.isSafeInteger(value) && Number(value) >= 0;
}
