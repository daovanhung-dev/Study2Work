import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { Subject, catchError, combineLatest, map, of, startWith, switchMap, tap } from 'rxjs';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { ME16CourseProgressService } from '../data-access/me16-course-progress.service';
import type { MentorCourseProgressRow, MentorPage } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

type ME16Result =
  | { courseId: string; response: ApiEnvelope<unknown> }
  | { courseId: string; error: unknown }
  | { courseId: null; invalid: true };

@Component({
  imports: [RouterLink, MentorPageHeader],
  selector: 'study-me16-page',
  styleUrls: ['./me16-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me16-page.html',
})
export class ME16Page implements OnInit {
  private readonly data = inject(ME16CourseProgressService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly route = inject(ActivatedRoute);
  private readonly reload$ = new Subject<void>();

  readonly courseId = signal('');
  readonly rows = signal<MentorCourseProgressRow[]>([]);
  readonly failedStudentAvatarIds = signal<ReadonlySet<string>>(new Set<string>());
  readonly total = signal(0);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly invalidId = signal(false);

  ngOnInit(): void {
    combineLatest([this.route.paramMap, this.reload$.pipe(startWith(undefined))])
      .pipe(
        map(([params]) => toSafeMentorId(params.get('courseId'))),
        tap((courseId) => this.resetRead(courseId)),
        switchMap((courseId) => {
          if (!courseId) return of<ME16Result>({ courseId: null, invalid: true });
          return this.data.progress(courseId).pipe(
            map((response): ME16Result => ({ courseId, response })),
            catchError((error: unknown) => of<ME16Result>({ courseId, error })),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyResult(result));
  }

  load(): void {
    if (this.courseId()) this.reload$.next();
  }

  safeId(value: unknown): string | null {
    return toSafeMentorId(value);
  }

  studentAvatarUrl(row: MentorCourseProgressRow): string | null {
    const id = toSafeMentorId(row.student.id);
    return id && !this.failedStudentAvatarIds().has(id)
      ? safeMentorAvatarUrl(row.student.avatar_url)
      : null;
  }

  studentInitials(row: MentorCourseProgressRow): string {
    const parts = row.student.full_name.trim().split(/\s+/).filter(Boolean);
    return parts.slice(-2).map((part) => Array.from(part)[0]?.toUpperCase() ?? '').join('') || '?';
  }

  markStudentAvatarFailed(studentId: unknown): void {
    const id = toSafeMentorId(studentId);
    if (!id) return;
    this.failedStudentAvatarIds.update((current) => new Set(current).add(id));
  }

  private resetRead(courseId: string | null): void {
    this.courseId.set(courseId ?? '');
    this.rows.set([]);
    this.failedStudentAvatarIds.set(new Set<string>());
    this.total.set(0);
    this.error.set(null);
    this.invalidId.set(!courseId);
    this.loading.set(Boolean(courseId));
  }

  private applyResult(result: ME16Result): void {
    if (result.courseId === null || this.courseId() !== result.courseId) return;
    if ('error' in result) {
      this.error.set(mentorApiErrorMessage(result.error));
      this.loading.set(false);
      return;
    }
    const envelope: unknown = result.response;
    if (!isApiEnvelope(envelope)) {
      this.error.set('Study Server trả về phản hồi tiến độ không hợp lệ.');
      this.loading.set(false);
      return;
    }
    if (!envelope.success) {
      this.error.set(envelope.message || 'Study Server không xác nhận dữ liệu tiến độ.');
      this.loading.set(false);
      return;
    }
    if (
      envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isCourseProgressPage(envelope.data)
    ) {
      this.error.set('Study Server trả về danh sách tiến độ không hợp lệ.');
      this.loading.set(false);
      return;
    }
    this.rows.set(envelope.data.items);
    this.total.set(envelope.data.pagination.total);
    this.loading.set(false);
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
    isRecord(value['data']) &&
    isRecord(value['meta']) &&
    typeof value['traceId'] === 'string'
  );
}

function isCourseProgressPage(value: unknown): value is MentorPage<MentorCourseProgressRow> {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) return false;
  const pagination = value['pagination'];
  const { page, size, total, total_pages: totalPages } = pagination;
  if (
    page !== 1 ||
    !isNonNegativeInt(size) ||
    !isNonNegativeInt(total) ||
    size !== total ||
    total !== value['items'].length ||
    totalPages !== (total === 0 ? 0 : 1)
  ) {
    return false;
  }

  const ids = new Set<string>();
  for (const row of value['items']) {
    if (
      !isRecord(row) ||
      !isRecord(row['student']) ||
      toSafeMentorId(row['student']['id']) === null ||
      typeof row['student']['full_name'] !== 'string' ||
      !isOptionalString(row['student']['avatar_url']) ||
      !isNonNegativeInt(row['completed_lessons']) ||
      !isNonNegativeInt(row['total_lessons']) ||
      row['completed_lessons'] > row['total_lessons'] ||
      !isNonNegativeInt(row['progress_percent']) ||
      row['progress_percent'] > 100
    ) {
      return false;
    }
    const id = toSafeMentorId(row['student']['id']);
    if (!id || ids.has(id)) return false;
    ids.add(id);
  }
  return true;
}

function isOptionalString(value: unknown): boolean {
  return value === undefined || value === null || typeof value === 'string';
}

function isNonNegativeInt(value: unknown): value is number {
  return Number.isSafeInteger(value) && Number(value) >= 0;
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
