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

import { ME05LectureDetailService } from '../data-access/me05-lecture-detail.service';
import type { MentorLecture } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

type LectureLoadResult =
  | { lectureId: string; response: ApiEnvelope<MentorLecture> }
  | { lectureId: string; error: unknown };

@Component({
  imports: [RouterLink, MentorPageHeader],
  selector: 'study-me05-page',
  styleUrls: ['./me05-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me05-page.html',
})
export class ME05Page implements OnInit {
  private readonly data = inject(ME05LectureDetailService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly route = inject(ActivatedRoute);
  private readonly retry$ = new Subject<void>();

  readonly lectureId = signal<string | null>(null);
  readonly lecture = signal<MentorLecture | null>(null);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly invalidId = signal(false);
  readonly notFound = signal(false);
  readonly accessDenied = signal(false);

  ngOnInit(): void {
    this.route.paramMap
      .pipe(
        map((params) => toSafeMentorId(params.get('lectureId'))),
        distinctUntilChanged(),
        tap((id) => this.resetForLecture(id)),
        switchMap((id) => {
          if (!id) return EMPTY;
          return this.retry$.pipe(
            startWith(undefined),
            tap(() => this.resetRequestState()),
            switchMap(() =>
              this.data.detail(id).pipe(
                map((response): LectureLoadResult => ({ lectureId: id, response })),
                catchError((error: unknown) => of<LectureLoadResult>({ lectureId: id, error })),
              ),
            ),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyResult(result));
  }

  load(): void {
    if (this.lectureId()) this.retry$.next();
  }

  private resetForLecture(id: string | null): void {
    this.lectureId.set(id);
    this.lecture.set(null);
    this.error.set(null);
    this.notFound.set(false);
    this.accessDenied.set(false);
    this.invalidId.set(id === null);
    this.loading.set(id !== null);
  }

  private resetRequestState(): void {
    this.lecture.set(null);
    this.error.set(null);
    this.notFound.set(false);
    this.accessDenied.set(false);
    this.loading.set(true);
  }

  private applyResult(result: LectureLoadResult): void {
    if (this.lectureId() !== result.lectureId) return;
    this.loading.set(false);

    if ('error' in result) {
      this.notFound.set(isHttpNotFound(result.error));
      this.accessDenied.set(isHttpForbidden(result.error));
      if (!this.notFound() && !this.accessDenied()) {
        this.error.set(mentorApiErrorMessage(result.error));
      }
      return;
    }

    const response: unknown = result.response;
    if (!isApiEnvelope(response)) {
      this.error.set('Study Server trả về phản hồi không hợp lệ.');
      return;
    }
    if (!response.success) {
      this.notFound.set(response.businessCode === 'DESIGN_RESOURCE_NOT_FOUND');
      if (!this.notFound()) {
        this.error.set(response.message || 'Study Server không xác nhận yêu cầu.');
      }
      return;
    }

    if (
      response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isLecture(response.data, result.lectureId)
    ) {
      this.error.set('Study Server trả về dữ liệu bài giảng không hợp lệ.');
      return;
    }

    this.lecture.set(response.data);
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

function isLecture(value: unknown, requestedId: string): value is MentorLecture {
  return (
    isRecord(value) &&
    toSafeMentorId(value['id']) === requestedId &&
    toSafeMentorId(value['course_id']) !== null &&
    typeof value['title'] === 'string' &&
    (typeof value['content'] === 'string' || value['content'] === null) &&
    Array.isArray(value['assets']) &&
    value['assets'].every(isUploadAsset) &&
    Number.isSafeInteger(value['order']) &&
    typeof value['status'] === 'string'
  );
}

function isUploadAsset(value: unknown): boolean {
  return (
    isRecord(value) &&
    toSafeMentorId(value['id']) !== null &&
    typeof value['name'] === 'string' &&
    typeof value['url'] === 'string' &&
    typeof value['content_type'] === 'string' &&
    Number.isSafeInteger(value['size_bytes']) &&
    Number(value['size_bytes']) >= 0 &&
    typeof value['status'] === 'string'
  );
}

function isHttpNotFound(error: unknown): boolean {
  return isHttpStatus(error, 404);
}

function isHttpForbidden(error: unknown): boolean {
  return isHttpStatus(error, 403);
}

function isHttpStatus(error: unknown, status: number): boolean {
  return isRecord(error) && error['status'] === status;
}
