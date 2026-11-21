import { DatePipe } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Subject, catchError, map, of, switchMap, tap } from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ME11SupportInboxService } from '../data-access/me11-support-inbox.service';
import type { MentorSupportRequest } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

type ME11Query = { courseId: string; status: string };
type ME11Result =
  | { query: ME11Query; response: ApiEnvelope<MentorSupportRequest[]> }
  | { query: ME11Query; error: unknown };

@Component({
  imports: [DatePipe, RouterLink, MentorPageHeader],
  selector: 'study-me11-page',
  styleUrls: ['./me11-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me11-page.html',
})
export class ME11Page implements OnInit {
  private readonly data = inject(ME11SupportInboxService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly query$ = new Subject<ME11Query>();

  readonly requests = signal<MentorSupportRequest[]>([]);
  readonly failedAvatarIds = signal<ReadonlySet<string>>(new Set());
  readonly courseFilter = signal('');
  readonly statusFilter = signal('');
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly forbidden = signal(false);

  ngOnInit(): void {
    this.query$
      .pipe(
        tap((query) => this.resetForQuery(query)),
        switchMap((query) =>
          this.data.list(query.courseId, query.status).pipe(
            map((response): ME11Result => ({ query, response })),
            catchError((error: unknown) => of<ME11Result>({ query, error })),
          ),
        ),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyResult(result));
    this.load();
  }

  load(courseId = this.courseFilter(), status = this.statusFilter()): void {
    const normalizedCourseId = courseId.trim();
    const normalizedStatus = status.trim();
    if (normalizedCourseId && !toSafeMentorId(normalizedCourseId)) {
      this.loading.set(false);
      this.error.set('Course ID cần là số nguyên dương int64.');
      this.forbidden.set(false);
      return;
    }
    this.query$.next({ courseId: normalizedCourseId, status: normalizedStatus });
  }

  apply(courseId: string, status: string): void {
    this.load(courseId, status);
  }

  safeId(value: unknown): string | null {
    return toSafeMentorId(value);
  }

  studentAvatarUrl(request: MentorSupportRequest): string | null {
    const studentId = toSafeMentorId(request.student.id);
    return studentId && !this.failedAvatarIds().has(studentId)
      ? safeMentorAvatarUrl(request.student.avatar_url)
      : null;
  }

  studentInitials(request: MentorSupportRequest): string {
    const parts = request.student.full_name.trim().split(/\s+/).filter(Boolean);
    return parts.slice(-2).map((part) => Array.from(part)[0]?.toUpperCase() ?? '').join('') || '?';
  }

  markStudentAvatarFailed(studentId: unknown): void {
    const id = toSafeMentorId(studentId);
    if (!id) return;
    this.failedAvatarIds.update((current) => new Set(current).add(id));
  }

  lastMessage(request: MentorSupportRequest): string {
    const messages = request.messages;
    return messages.length ? messages[messages.length - 1].content : 'Chưa có tin nhắn.';
  }

  private resetForQuery(query: ME11Query): void {
    this.courseFilter.set(query.courseId);
    this.statusFilter.set(query.status);
    this.requests.set([]);
    this.failedAvatarIds.set(new Set());
    this.loading.set(true);
    this.error.set(null);
    this.forbidden.set(false);
  }

  private applyResult(result: ME11Result): void {
    if (this.courseFilter() !== result.query.courseId || this.statusFilter() !== result.query.status) return;
    this.loading.set(false);

    if ('error' in result) {
      this.forbidden.set(hasHttpStatus(result.error, 403));
      if (!this.forbidden()) this.error.set(mentorApiErrorMessage(result.error));
      return;
    }

    const envelope: unknown = result.response;
    if (!isApiEnvelope(envelope)) {
      this.error.set('Study Server trả về phản hồi không hợp lệ.');
      return;
    }
    if (!envelope.success) {
      this.forbidden.set(envelope.businessCode === 'DESIGN_ACCESS_DENIED');
      if (!this.forbidden()) this.error.set(envelope.message || 'Study Server không xác nhận yêu cầu.');
      return;
    }
    if (envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' || !isSupportRequestList(envelope.data)) {
      this.error.set('Study Server trả về danh sách hỗ trợ không hợp lệ.');
      return;
    }
    this.requests.set(envelope.data);
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

function isSupportRequestList(value: unknown): value is MentorSupportRequest[] {
  if (!Array.isArray(value)) return false;
  const requestIds = new Set<string>();
  for (const request of value) {
    if (!isSupportRequest(request)) return false;
    const id = toSafeMentorId(request['id']);
    if (id === null || requestIds.has(id)) return false;
    requestIds.add(id);
  }
  return true;
}

function isSupportRequest(value: unknown): value is MentorSupportRequest {
  if (
    !isRecord(value) ||
    toSafeMentorId(value['id']) === null ||
    toSafeMentorId(value['course_id']) === null ||
    typeof value['status'] !== 'string' ||
    !isUserSummary(value['student']) ||
    !Array.isArray(value['messages']) ||
    !isDateTime(value['created_at']) ||
    (value['resolved_at'] !== undefined && value['resolved_at'] !== null && !isDateTime(value['resolved_at']))
  ) {
    return false;
  }
  const messageIds = new Set<string>();
  for (const message of value['messages']) {
    if (!isSupportMessage(message)) return false;
    const id = toSafeMentorId(message['id']);
    if (id === null || messageIds.has(id)) return false;
    messageIds.add(id);
  }
  return true;
}

function isSupportMessage(value: unknown): boolean {
  return (
    isRecord(value) &&
    toSafeMentorId(value['id']) !== null &&
    isUserSummary(value['author']) &&
    typeof value['content'] === 'string' &&
    isDateTime(value['created_at']) &&
    Array.isArray(value['attachments']) &&
    value['attachments'].every(isUploadAsset)
  );
}

function isUserSummary(value: unknown): boolean {
  return (
    isRecord(value) &&
    toSafeMentorId(value['id']) !== null &&
    typeof value['full_name'] === 'string' &&
    (value['avatar_url'] === undefined || value['avatar_url'] === null || typeof value['avatar_url'] === 'string')
  );
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

function isDateTime(value: unknown): value is string {
  return typeof value === 'string' && !Number.isNaN(Date.parse(value));
}

function hasHttpStatus(error: unknown, status: number): boolean {
  return isRecord(error) && error['status'] === status;
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
