import { DatePipe } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { Subject, catchError, combineLatest, map, of, startWith, switchMap, tap } from 'rxjs';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { ME17StudentProgressService } from '../data-access/me17-student-progress.service';
import type { MentorStudentProgress } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

type ME17Result =
  | { courseId: string; studentId: string; response: ApiEnvelope<unknown> }
  | { courseId: string; studentId: string; error: unknown }
  | { courseId: null; studentId: null; invalid: true };

@Component({
  imports: [DatePipe, RouterLink, MentorPageHeader],
  selector: 'study-me17-page',
  styleUrls: ['./me17-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me17-page.html',
})
export class ME17Page implements OnInit {
  private readonly data = inject(ME17StudentProgressService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly route = inject(ActivatedRoute);
  private readonly reload$ = new Subject<void>();

  readonly courseId = signal('');
  readonly studentId = signal('');
  readonly progress = signal<MentorStudentProgress | null>(null);
  readonly failedStudentAvatar = signal(false);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly invalidRoute = signal(false);

  ngOnInit(): void {
    combineLatest([this.route.paramMap, this.reload$.pipe(startWith(undefined))])
      .pipe(
        map(([params]) => ({
          courseId: toSafeMentorId(params.get('courseId')),
          studentId: toSafeMentorId(params.get('studentId')),
        })),
        tap(({ courseId, studentId }) => this.resetRead(courseId, studentId)),
        switchMap(({ courseId, studentId }) => {
          if (!courseId || !studentId) {
            return of<ME17Result>({ courseId: null, studentId: null, invalid: true });
          }
          return this.data.progress(courseId, studentId).pipe(
            map((response): ME17Result => ({ courseId, studentId, response })),
            catchError((error: unknown) => of<ME17Result>({ courseId, studentId, error })),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyResult(result));
  }

  load(): void {
    if (this.courseId() && this.studentId()) this.reload$.next();
  }

  safeLessonId(value: unknown): string | null {
    return toSafeMentorId(value);
  }

  studentAvatarUrl(item: MentorStudentProgress): string | null {
    return !this.failedStudentAvatar() ? safeMentorAvatarUrl(item.student.avatar_url) : null;
  }

  studentInitials(fullName: string): string {
    const parts = fullName.trim().split(/\s+/).filter(Boolean);
    return parts.slice(-2).map((part) => Array.from(part)[0]?.toUpperCase() ?? '').join('') || '?';
  }

  markStudentAvatarFailed(): void {
    this.failedStudentAvatar.set(true);
  }

  private resetRead(courseId: string | null, studentId: string | null): void {
    this.courseId.set(courseId ?? '');
    this.studentId.set(studentId ?? '');
    this.progress.set(null);
    this.failedStudentAvatar.set(false);
    this.error.set(null);
    this.invalidRoute.set(!courseId || !studentId);
    this.loading.set(Boolean(courseId && studentId));
  }

  private applyResult(result: ME17Result): void {
    if (result.courseId === null || result.studentId === null) return;
    if (this.courseId() !== result.courseId || this.studentId() !== result.studentId) return;
    if ('error' in result) {
      this.error.set(mentorApiErrorMessage(result.error));
      this.loading.set(false);
      return;
    }
    const envelope: unknown = result.response;
    if (!isApiEnvelope(envelope)) {
      this.error.set('Study Server trả về phản hồi snapshot không hợp lệ.');
      this.loading.set(false);
      return;
    }
    if (!envelope.success) {
      this.error.set(envelope.message || 'Study Server không xác nhận snapshot tiến độ.');
      this.loading.set(false);
      return;
    }
    if (
      envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isStudentProgress(envelope.data, result.courseId, result.studentId)
    ) {
      this.error.set('Study Server trả về snapshot không khớp với course/student hoặc không hợp lệ.');
      this.loading.set(false);
      return;
    }
    this.progress.set(envelope.data);
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

function isStudentProgress(value: unknown, courseId: string, studentId: string): value is MentorStudentProgress {
  if (!isRecord(value) || !isRecord(value['student']) || !isRecord(value['summary']) || !Array.isArray(value['lessons'])) return false;
  const student = value['student'];
  const summary = value['summary'];
  if (
    toSafeMentorId(value['course_id']) !== courseId ||
    toSafeMentorId(student['id']) !== studentId ||
    typeof student['full_name'] !== 'string' ||
    !isOptionalString(student['avatar_url'])
  ) {
    return false;
  }

  const lessonIds = new Set<string>();
  let completedCount = 0;
  let percentSum = 0;
  let previousOrder: number | null = null;
  let previousId = 0n;
  for (const lesson of value['lessons']) {
    if (
      !isRecord(lesson) ||
      toSafeMentorId(lesson['lesson_id']) === null ||
      typeof lesson['title'] !== 'string' ||
      !Number.isSafeInteger(lesson['order']) ||
      !['NOT_STARTED', 'IN_PROGRESS', 'COMPLETED'].includes(String(lesson['progress_status'])) ||
      !isPercent(lesson['progress_percent']) ||
      !isNullableDateTime(lesson['last_accessed_at']) ||
      !isNullableDateTime(lesson['completed_at'])
    ) {
      return false;
    }
    const lessonId = toSafeMentorId(lesson['lesson_id']);
    if (!lessonId || lessonIds.has(lessonId)) return false;
    const numericId = BigInt(lessonId);
    const order = Number(lesson['order']);
    if (previousOrder !== null && (order < previousOrder || (order === previousOrder && numericId <= previousId))) return false;
    previousOrder = order;
    previousId = numericId;
    lessonIds.add(lessonId);
    if (lesson['progress_status'] === 'COMPLETED') completedCount += 1;
    percentSum += Number(lesson['progress_percent']);
  }

  const totalLessons = value['lessons'].length;
  const expectedPercent = totalLessons ? Math.floor(percentSum / totalLessons) : 0;
  return (
    isNonNegativeInt(summary['completed_lessons']) &&
    isNonNegativeInt(summary['total_lessons']) &&
    summary['total_lessons'] === totalLessons &&
    summary['completed_lessons'] === completedCount &&
    isPercent(summary['progress_percent']) &&
    summary['progress_percent'] === expectedPercent
  );
}

function isOptionalString(value: unknown): boolean {
  return value === undefined || value === null || typeof value === 'string';
}

function isNonNegativeInt(value: unknown): value is number {
  return Number.isSafeInteger(value) && Number(value) >= 0;
}

function isPercent(value: unknown): value is number {
  return isNonNegativeInt(value) && value <= 100;
}

function isNullableDateTime(value: unknown): boolean {
  return value === null || (typeof value === 'string' && value.length > 0 && Number.isFinite(Date.parse(value)));
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
