import { DatePipe } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Subject, catchError, defer, map, of, startWith, switchMap, tap } from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ME01DashboardService } from '../data-access/me01-dashboard.service';
import type { MentorCourse, MentorPage, MentorSubmission, MentorSupportRequest } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({
  imports: [DatePipe, RouterLink, MentorPageHeader],
  selector: 'study-me01-page',
  styleUrls: ['./me01-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me01-page.html',
})
export class ME01Page implements OnInit {
  private readonly data = inject(ME01DashboardService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly courseReload$ = new Subject<void>();
  private readonly submissionReload$ = new Subject<void>();
  private readonly supportReload$ = new Subject<void>();
  readonly courses = signal<MentorCourse[]>([]);
  readonly submissions = signal<MentorSubmission[]>([]);
  readonly supportRequests = signal<MentorSupportRequest[]>([]);
  readonly courseLoading = signal(true);
  readonly submissionLoading = signal(true);
  readonly supportLoading = signal(true);
  readonly courseError = signal<string | null>(null);
  readonly submissionError = signal<string | null>(null);
  readonly supportError = signal<string | null>(null);

  ngOnInit(): void {
    this.courseReload$.pipe(
      startWith(undefined),
      tap(() => { this.courseLoading.set(true); this.courseError.set(null); }),
      switchMap(() => defer(() => this.data.courses()).pipe(
        map((response) => ({ response })),
        catchError((error: unknown) => of({ error })),
      )),
      takeUntilDestroyed(this.destroyRef),
    ).subscribe((result) => {
      this.courseLoading.set(false);
      if ('error' in result) {
        this.courseError.set(mentorApiErrorMessage(result.error));
      } else if (!isEnvelope(result.response) || !result.response.success) {
        this.courseError.set(isEnvelope(result.response)
          ? mentorEnvelopeError(result.response.success, result.response.message)
          : 'Study Server trả về phản hồi khóa học không hợp lệ.');
      } else if (
        result.response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
        !isMentorPage(result.response.data, 4, isCoursePreview)
      ) {
        this.courseError.set('Study Server trả về danh sách khóa học không hợp lệ.');
      } else {
        this.courses.set(result.response.data.items);
      }
    });

    this.submissionReload$.pipe(
      startWith(undefined),
      tap(() => { this.submissionLoading.set(true); this.submissionError.set(null); }),
      switchMap(() => defer(() => this.data.submissions()).pipe(
        map((response) => ({ response })),
        catchError((error: unknown) => of({ error })),
      )),
      takeUntilDestroyed(this.destroyRef),
    ).subscribe((result) => {
      this.submissionLoading.set(false);
      if ('error' in result) {
        this.submissionError.set(mentorApiErrorMessage(result.error));
      } else if (!isEnvelope(result.response) || !result.response.success) {
        this.submissionError.set(isEnvelope(result.response)
          ? mentorEnvelopeError(result.response.success, result.response.message)
          : 'Study Server trả về phản hồi bài nộp không hợp lệ.');
      } else if (
        result.response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
        !isMentorPage(result.response.data, 20, isSubmissionPreview)
      ) {
        this.submissionError.set('Study Server trả về danh sách bài nộp không hợp lệ.');
      } else {
        this.submissions.set(result.response.data.items.slice(0, 4));
      }
    });

    this.supportReload$.pipe(
      startWith(undefined),
      tap(() => { this.supportLoading.set(true); this.supportError.set(null); }),
      switchMap(() => defer(() => this.data.support()).pipe(
        map((response) => ({ response })),
        catchError((error: unknown) => of({ error })),
      )),
      takeUntilDestroyed(this.destroyRef),
    ).subscribe((result) => {
      this.supportLoading.set(false);
      if ('error' in result) {
        this.supportError.set(mentorApiErrorMessage(result.error));
      } else if (!isEnvelope(result.response) || !result.response.success) {
        this.supportError.set(isEnvelope(result.response)
          ? mentorEnvelopeError(result.response.success, result.response.message)
          : 'Study Server trả về phản hồi hỗ trợ không hợp lệ.');
      } else if (
        result.response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
        !Array.isArray(result.response.data) ||
        !result.response.data.every(isSupportPreview)
      ) {
        this.supportError.set('Study Server trả về danh sách yêu cầu hỗ trợ không hợp lệ.');
      } else {
        this.supportRequests.set(result.response.data.slice(0, 4));
      }
    });
  }

  load(): void {
    this.courseReload$.next();
    this.submissionReload$.next();
    this.supportReload$.next();
  }

  reloadCourses(): void { this.courseReload$.next(); }
  reloadSubmissions(): void { this.submissionReload$.next(); }
  reloadSupport(): void { this.supportReload$.next(); }

  safeId(value: unknown): string | null { return toSafeMentorId(value); }
  lastMessage(request: MentorSupportRequest): string { return request.messages.at(-1)?.content ?? 'Chưa có nội dung trao đổi.'; }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isEnvelope<T>(value: unknown): value is ApiEnvelope<T> {
  return isRecord(value) &&
    typeof value['success'] === 'boolean' &&
    typeof value['businessCode'] === 'string' &&
    typeof value['message'] === 'string' &&
    isRecord(value['meta']) &&
    typeof value['traceId'] === 'string';
}

function isMentorPage<T>(value: unknown, expectedSize: number, isItem: (item: unknown) => item is T): value is MentorPage<T> {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) return false;
  const pagination = value['pagination'];
  const { page, size, total, total_pages: totalPages } = pagination;
  return Number.isSafeInteger(page) && page === 1 &&
    Number.isSafeInteger(size) && size === expectedSize &&
    Number.isSafeInteger(total) && Number(total) >= 0 &&
    Number.isSafeInteger(totalPages) && totalPages === (total === 0 ? 0 : Math.ceil(Number(total) / expectedSize)) &&
    value['items'].length <= expectedSize && value['items'].every(isItem);
}

function isCoursePreview(value: unknown): value is MentorCourse {
  if (!isRecord(value) || !isRecord(value['mentor'])) return false;
  return toSafeMentorId(value['id']) !== null &&
    typeof value['title'] === 'string' &&
    isOptionalNullableString(value, 'description') &&
    isOptionalNullableString(value, 'thumbnail_url') &&
    typeof value['price'] === 'string' &&
    (value['status'] === 'DRAFT' || value['status'] === 'PUBLISHED') &&
    toSafeMentorId(value['mentor']['id']) !== null &&
    typeof value['mentor']['full_name'] === 'string' &&
    isOptionalNullableString(value['mentor'], 'avatar_url');
}

function isSubmissionPreview(value: unknown): value is MentorSubmission {
  return isRecord(value) && toSafeMentorId(value['id']) !== null &&
    toSafeMentorId(value['assignment_id']) !== null && toSafeMentorId(value['user_id']) !== null &&
    typeof value['status'] === 'string' && isDateTime(value['submitted_at']) &&
    isOptionalNullableString(value, 'content') && isOptionalNullableString(value, 'score') &&
    isOptionalNullableString(value, 'feedback') && Array.isArray(value['files']) &&
    value['files'].every(isUploadPreview);
}

function isSupportPreview(value: unknown): value is MentorSupportRequest {
  return isRecord(value) && toSafeMentorId(value['id']) !== null &&
    toSafeMentorId(value['course_id']) !== null &&
    typeof value['status'] === 'string' && isDateTime(value['created_at']) &&
    isOptionalNullableString(value, 'resolved_at') &&
    isRecord(value['student']) && toSafeMentorId(value['student']['id']) !== null &&
    typeof value['student']['full_name'] === 'string' &&
    isOptionalNullableString(value['student'], 'avatar_url') &&
    Array.isArray(value['messages']) && value['messages'].every((message) =>
      isRecord(message) && toSafeMentorId(message['id']) !== null &&
      isRecord(message['author']) && toSafeMentorId(message['author']['id']) !== null &&
      typeof message['author']['full_name'] === 'string' &&
      isOptionalNullableString(message['author'], 'avatar_url') &&
      typeof message['content'] === 'string' && isDateTime(message['created_at']) &&
      Array.isArray(message['attachments']) && message['attachments'].every(isUploadPreview));
}

function isUploadPreview(value: unknown): boolean {
  return isRecord(value) && toSafeMentorId(value['id']) !== null &&
    typeof value['name'] === 'string' && typeof value['url'] === 'string' &&
    typeof value['content_type'] === 'string' && Number.isSafeInteger(value['size_bytes']) &&
    Number(value['size_bytes']) >= 0 && typeof value['status'] === 'string';
}

function isOptionalNullableString(record: Record<string, unknown>, field: string): boolean {
  return !(field in record) || record[field] === null || typeof record[field] === 'string';
}

function isDateTime(value: unknown): value is string {
  return typeof value === 'string' && value.length > 0 && Number.isFinite(Date.parse(value));
}
