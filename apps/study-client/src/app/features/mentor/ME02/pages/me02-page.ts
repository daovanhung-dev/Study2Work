import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Subject, catchError, defer, map, of, switchMap } from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ME02CoursesService } from '../data-access/me02-courses.service';
import type { MentorCourse, MentorPage } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

const ME02_PAGE_SIZE = 20;
const COURSE_STATUSES = ['DRAFT', 'PUBLISHED'] as const;

type ME02Request = { page: number; status: string };
type ME02LoadResult =
  | { page: number; status: string; response: ApiEnvelope<unknown> }
  | { page: number; status: string; error: unknown };

@Component({
  imports: [RouterLink, MentorPageHeader],
  selector: 'study-me02-page',
  styleUrls: ['./me02-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me02-page.html',
})
export class ME02Page implements OnInit {
  private readonly data = inject(ME02CoursesService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly requests$ = new Subject<ME02Request>();

  readonly courses = signal<MentorCourse[]>([]);
  readonly page = signal(1);
  readonly total = signal(0);
  readonly totalPages = signal(0);
  readonly status = signal('');
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly failedThumbnailUrls = signal<ReadonlySet<string>>(new Set());

  ngOnInit(): void {
    this.requests$
      .pipe(
        switchMap(({ page, status }) =>
          defer(() => this.data.list(page, status)).pipe(
            map((response) => ({ page, status, response })),
            catchError((error: unknown) => of({ page, status, error })),
          ),
        ),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyResult(result));

    this.load();
  }

  load(page = this.page(), status = this.status()): void {
    const nextPage = Number.isSafeInteger(page) && page > 0 ? page : 1;
    const nextStatus = normalizeCourseStatus(status);
    this.page.set(nextPage);
    this.status.set(nextStatus);
    this.courses.set([]);
    this.total.set(0);
    this.totalPages.set(0);
    this.loading.set(true);
    this.error.set(null);
    this.requests$.next({ page: nextPage, status: nextStatus });
  }

  filter(status: string): void {
    this.load(1, status);
  }

  safeId(value: unknown): string | null {
    return toSafeMentorId(value);
  }

  statusLabel(status: string): string {
    switch (status) {
      case 'DRAFT':
        return 'Bản nháp';
      case 'PUBLISHED':
        return 'Đã xuất bản';
      default:
        return 'Trạng thái chưa xác định';
    }
  }

  thumbnailUrl(course: MentorCourse): string | null {
    const source = course.thumbnail_url?.trim();
    if (!source) return null;

    try {
      const origin = typeof window === 'undefined' ? null : window.location.origin;
      const url = origin ? new URL(source, origin) : new URL(source);
      if (url.protocol === 'https:' || (origin !== null && url.protocol === 'http:' && url.origin === origin)) {
        return url.href;
      }
    } catch {
      return null;
    }
    return null;
  }

  thumbnailFailed(url: string): boolean {
    return this.failedThumbnailUrls().has(url);
  }

  markThumbnailFailed(url: string): void {
    this.failedThumbnailUrls.update((current) => new Set(current).add(url));
  }

  private applyResult(result: ME02LoadResult): void {
    if (result.page !== this.page() || result.status !== this.status()) return;
    this.loading.set(false);

    if ('error' in result) {
      this.error.set(mentorApiErrorMessage(result.error));
      return;
    }

    const response: unknown = result.response;
    if (!isApiEnvelope(response)) {
      this.error.set('Study Server trả về phản hồi không hợp lệ.');
      return;
    }
    if (!response.success) {
      this.error.set(mentorEnvelopeError(response.success, response.message));
      return;
    }
    if (
      response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isCoursePage(response.data, result.page, result.status)
    ) {
      this.error.set('Study Server trả về dữ liệu khóa học không hợp lệ.');
      return;
    }

    const coursePage = response.data;
    const lastValidPage = Math.max(coursePage.pagination.total_pages, 1);
    if (coursePage.items.length === 0 && result.page > lastValidPage) {
      this.load(lastValidPage, result.status);
      return;
    }

    this.courses.set(coursePage.items);
    this.total.set(coursePage.pagination.total);
    this.totalPages.set(coursePage.pagination.total_pages);
  }
}

function normalizeCourseStatus(status: string): string {
  return COURSE_STATUSES.includes(status as (typeof COURSE_STATUSES)[number]) ? status : '';
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

function isCoursePage(value: unknown, requestedPage: number, requestedStatus: string): value is MentorPage<MentorCourse> {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) return false;

  const pagination = value['pagination'];
  const { page, size, total, total_pages: totalPages } = pagination;
  if (
    !Number.isSafeInteger(page) ||
    page !== requestedPage ||
    size !== ME02_PAGE_SIZE ||
    !Number.isSafeInteger(total) ||
    (total as number) < 0 ||
    !Number.isSafeInteger(totalPages) ||
    totalPages !== ((total as number) === 0 ? 0 : Math.ceil((total as number) / ME02_PAGE_SIZE)) ||
    (value['items'] as unknown[]).length > ME02_PAGE_SIZE
  ) {
    return false;
  }

  return (value['items'] as unknown[]).every((course) => isMentorCourse(course, requestedStatus));
}

function isMentorCourse(value: unknown, requestedStatus: string): value is MentorCourse {
  if (!isRecord(value) || !isRecord(value['mentor'])) return false;
  const mentor = value['mentor'];
  const status = value['status'];
  return (
    Number.isSafeInteger(value['id']) &&
    (value['id'] as number) > 0 &&
    typeof value['title'] === 'string' &&
    isOptionalNullableString(value, 'description') &&
    isOptionalNullableString(value, 'thumbnail_url') &&
    typeof value['price'] === 'string' &&
    COURSE_STATUSES.includes(status as (typeof COURSE_STATUSES)[number]) &&
    (!requestedStatus || status === requestedStatus) &&
    Number.isSafeInteger(mentor['id']) &&
    (mentor['id'] as number) > 0 &&
    typeof mentor['full_name'] === 'string' &&
    isOptionalNullableString(mentor, 'avatar_url')
  );
}

function isOptionalNullableString(record: Record<string, unknown>, field: string): boolean {
  return !(field in record) || record[field] === null || typeof record[field] === 'string';
}
