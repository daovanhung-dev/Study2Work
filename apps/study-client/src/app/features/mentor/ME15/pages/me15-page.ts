import { DatePipe } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { Subject, catchError, combineLatest, map, of, startWith, switchMap, tap } from 'rxjs';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { ME15NotificationStatusService } from '../data-access/me15-notification-status.service';
import type { MentorNotificationOperation } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

type ME15StatusResult =
  | { notificationId: string; response: ApiEnvelope<unknown> }
  | { notificationId: string; error: unknown }
  | { notificationId: null; invalid: true };

@Component({
  imports: [DatePipe, RouterLink, MentorPageHeader],
  selector: 'study-me15-page',
  styleUrls: ['./me15-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me15-page.html',
})
export class ME15Page implements OnInit {
  private readonly data = inject(ME15NotificationStatusService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly route = inject(ActivatedRoute);
  private readonly reload$ = new Subject<void>();

  readonly notificationId = signal('');
  readonly operation = signal<MentorNotificationOperation | null>(null);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly invalidId = signal(false);

  ngOnInit(): void {
    combineLatest([
      this.route.paramMap,
      this.reload$.pipe(startWith(undefined)),
    ])
      .pipe(
        map(([params]) => toSafeMentorId(params.get('notificationId'))),
        tap((notificationId) => this.resetRead(notificationId)),
        switchMap((notificationId) => {
          if (!notificationId) return of<ME15StatusResult>({ notificationId: null, invalid: true });
          return this.data.status(notificationId).pipe(
            map((response): ME15StatusResult => ({ notificationId, response })),
            catchError((error: unknown) => of<ME15StatusResult>({ notificationId, error })),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyResult(result));
  }

  load(): void {
    if (this.notificationId()) this.reload$.next();
  }

  private resetRead(notificationId: string | null): void {
    this.notificationId.set(notificationId ?? '');
    this.operation.set(null);
    this.error.set(null);
    this.invalidId.set(!notificationId);
    this.loading.set(Boolean(notificationId));
  }

  private applyResult(result: ME15StatusResult): void {
    if (result.notificationId === null) return;
    if (this.notificationId() !== result.notificationId) return;
    if ('error' in result) {
      this.error.set(mentorApiErrorMessage(result.error));
      this.loading.set(false);
      return;
    }

    const envelope: unknown = result.response;
    if (!isApiEnvelope(envelope)) {
      this.error.set('Study Server trả về phản hồi trạng thái không hợp lệ.');
      this.loading.set(false);
      return;
    }
    if (!envelope.success) {
      this.error.set(envelope.message || 'Study Server không xác nhận trạng thái notification.');
      this.loading.set(false);
      return;
    }
    if (
      envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isNotificationOperation(envelope.data)
    ) {
      this.error.set('Study Server trả về trạng thái notification không hợp lệ.');
      this.loading.set(false);
      return;
    }

    this.operation.set(envelope.data);
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

function isNotificationOperation(value: unknown): value is MentorNotificationOperation {
  if (!isRecord(value)) return false;
  return (
    typeof value['id'] === 'string' &&
    /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value['id']) &&
    value['kind'] === 'NOTIFICATION_DISPATCH' &&
    (value['status'] === 'QUEUED' || value['status'] === 'SENT' || value['status'] === 'FAILED') &&
    toSafeMentorId(value['owner_id']) !== null &&
    isDateTime(value['submitted_at']) &&
    isDateTime(value['updated_at']) &&
    (value['completed_at'] === undefined || value['completed_at'] === null || isDateTime(value['completed_at']))
  );
}

function isDateTime(value: unknown): value is string {
  return typeof value === 'string' && value.length > 0 && Number.isFinite(Date.parse(value));
}
