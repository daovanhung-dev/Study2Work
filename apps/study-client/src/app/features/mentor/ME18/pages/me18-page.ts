import { DatePipe } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { Subject, catchError, combineLatest, map, of, startWith, switchMap, tap } from 'rxjs';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { ME18AnalyticsService } from '../data-access/me18-analytics.service';
import type { MentorCourseAnalytics } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

type ME18Result =
  | { courseId: string; response: ApiEnvelope<unknown> }
  | { courseId: string; error: unknown }
  | { courseId: null; invalid: true };

@Component({
  imports: [DatePipe, RouterLink, MentorPageHeader],
  selector: 'study-me18-page',
  styleUrls: ['./me18-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me18-page.html',
})
export class ME18Page implements OnInit {
  private readonly data = inject(ME18AnalyticsService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly route = inject(ActivatedRoute);
  private readonly reload$ = new Subject<void>();

  readonly courseId = signal('');
  readonly analytics = signal<MentorCourseAnalytics | null>(null);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly invalidId = signal(false);

  ngOnInit(): void {
    combineLatest([this.route.paramMap, this.reload$.pipe(startWith(undefined))])
      .pipe(
        map(([params]) => toSafeMentorId(params.get('courseId'))),
        tap((courseId) => this.resetRead(courseId)),
        switchMap((courseId) => {
          if (!courseId) return of<ME18Result>({ courseId: null, invalid: true });
          return this.data.load(courseId).pipe(
            map((response): ME18Result => ({ courseId, response })),
            catchError((error: unknown) => of<ME18Result>({ courseId, error })),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyResult(result));
  }

  load(): void {
    if (this.courseId()) this.reload$.next();
  }

  private resetRead(courseId: string | null): void {
    this.courseId.set(courseId ?? '');
    this.analytics.set(null);
    this.error.set(null);
    this.invalidId.set(!courseId);
    this.loading.set(Boolean(courseId));
  }

  private applyResult(result: ME18Result): void {
    if (result.courseId === null || this.courseId() !== result.courseId) return;
    if ('error' in result) {
      this.error.set(mentorApiErrorMessage(result.error));
      this.loading.set(false);
      return;
    }
    const envelope: unknown = result.response;
    if (!isApiEnvelope(envelope)) {
      this.error.set('Study Server trả về phản hồi analytics không hợp lệ.');
      this.loading.set(false);
      return;
    }
    if (!envelope.success) {
      this.error.set(envelope.message || 'Study Server không xác nhận analytics khóa học.');
      this.loading.set(false);
      return;
    }
    if (
      envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isCourseAnalytics(envelope.data)
    ) {
      this.error.set('Study Server trả về dữ liệu analytics không hợp lệ.');
      this.loading.set(false);
      return;
    }
    this.analytics.set(envelope.data);
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

function isCourseAnalytics(value: unknown): value is MentorCourseAnalytics {
  if (!isRecord(value)) return false;
  const trackedAccesses = value['tracked_lesson_accesses'];
  const studentsWithActivity = value['students_with_activity'];
  const lastActivityAt = value['last_activity_at'];
  if (
    !isNonNegativeInt64(trackedAccesses) ||
    !isNonNegativeInt64(studentsWithActivity) ||
    studentsWithActivity > trackedAccesses ||
    !isNullableDateTime(lastActivityAt)
  ) {
    return false;
  }
  return trackedAccesses === 0
    ? studentsWithActivity === 0 && lastActivityAt === null
    : studentsWithActivity > 0 && lastActivityAt !== null;
}

function isNonNegativeInt64(value: unknown): value is number {
  return Number.isSafeInteger(value) && Number(value) >= 0 && Number(value) <= 9_223_372_036_854_775_807;
}

function isNullableDateTime(value: unknown): boolean {
  return value === null || (typeof value === 'string' && value.length > 0 && Number.isFinite(Date.parse(value)));
}
