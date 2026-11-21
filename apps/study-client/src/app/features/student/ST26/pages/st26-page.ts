import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import {
  Subject,
  catchError,
  map,
  of,
  startWith,
  switchMap,
  tap,
} from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ST26NotificationsService } from '../data-access/st26-notifications.service';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import {
  isStudentNotificationPage,
  isStudentNotificationReadSummary,
  isStudentReadNotificationPage,
} from '../../shared/models/student-notification-page.guard';
import type {
  StudentNotification,
  StudentPage,
  StudentPagination,
} from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [RouterLink],
  selector: 'study-st26-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-community.css',
    './st26-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st26-page.html',
})
export class ST26Page implements OnInit {
  private readonly dateTimeFormatter = new Intl.DateTimeFormat('vi-VN', {
    dateStyle: 'medium',
    timeStyle: 'short',
  });
  private readonly dateFormatter = new Intl.DateTimeFormat('vi-VN', {
    dateStyle: 'long',
  });
  private readonly data = inject(ST26NotificationsService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly listRequests$ = new Subject<NotificationRequest>();
  private readonly unreadCountRequests$ = new Subject<void>();

  readonly unreadOnly = signal(false);
  readonly page = signal(1);
  readonly notifications = signal<StudentNotification[]>([]);
  readonly notificationGroups = computed(() => {
    const today = new Date();
    const todayKey = localDateKey(today);
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    const yesterdayKey = localDateKey(yesterday);
    const groups = new Map<string, NotificationDateGroup>();

    for (const item of this.notifications()) {
      const createdAt = new Date(item.created_at);
      const key = dateGroupKey(createdAt);
      const label = dateGroupLabel(
        key,
        createdAt,
        todayKey,
        yesterdayKey,
        this.dateFormatter,
      );
      const existingGroup = groups.get(key);

      if (existingGroup) {
        existingGroup.items.push(item);
      } else {
        groups.set(key, { key, label, items: [item] });
      }
    }

    return [...groups.values()];
  });
  readonly pagination = signal<StudentPagination | null>(null);
  readonly allCount = signal<number | null>(null);
  readonly unreadCount = signal<number | null>(null);
  readonly loading = signal(true);
  readonly loadingUnreadCount = signal(true);
  readonly markingId = signal<string | null>(null);
  readonly markingAll = signal(false);
  readonly error = signal<string | null>(null);
  readonly unreadCountError = signal<string | null>(null);
  readonly actionError = signal<string | null>(null);
  readonly actionMessage = signal<string | null>(null);

  ngOnInit(): void {
    this.listRequests$
      .pipe(
        tap(() => {
          this.loading.set(true);
          this.error.set(null);
          this.notifications.set([]);
          this.pagination.set(null);
        }),
        switchMap((request) =>
          this.data.list(request.unreadOnly, request.page).pipe(
            map((response) => ({ request, response, error: null })),
            catchError((error: unknown) => of({ request, response: null, error })),
          ),
        ),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyListResult(result));

    this.unreadCountRequests$
      .pipe(
        startWith(undefined),
        tap(() => {
          this.loadingUnreadCount.set(true);
          this.unreadCountError.set(null);
        }),
        switchMap(() =>
          this.data.list(true, 1).pipe(
            map((response) => ({ response, error: null })),
            catchError((error: unknown) => of({ response: null, error })),
          ),
        ),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyUnreadCountResult(result));

    this.load();
  }

  load(): void {
    this.listRequests$.next({ unreadOnly: this.unreadOnly(), page: this.page() });
  }

  retry(): void {
    this.load();
  }

  refreshUnreadCount(): void {
    this.unreadCountRequests$.next();
  }

  selectFilter(unreadOnly: boolean): void {
    if (this.unreadOnly() === unreadOnly) return;
    this.unreadOnly.set(unreadOnly);
    this.page.set(1);
    this.actionError.set(null);
    this.actionMessage.set(null);
    this.load();
  }

  changePage(delta: number): void {
    const next = this.page() + delta;
    const totalPages = this.pagination()?.total_pages ?? 0;
    if (next < 1 || next > totalPages) return;
    this.page.set(next);
    this.load();
  }

  safeId(value: unknown): string | null {
    return toSafeStudyId(value);
  }

  formatCreatedAt(value: string): string {
    const date = new Date(value);
    return Number.isNaN(date.getTime())
      ? 'Thời gian không xác định'
      : this.dateTimeFormatter.format(date);
  }

  markRead(notification: StudentNotification): void {
    const notificationId = toSafeStudyId(notification.id);
    if (
      !notificationId ||
      notification.is_read ||
      this.markingId() !== null ||
      this.markingAll()
    ) {
      return;
    }

    this.markingId.set(notificationId);
    this.actionError.set(null);
    this.actionMessage.set(null);
    this.data
      .markRead(notificationId)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          this.markingId.set(null);
          if (
            !response.success ||
            response.businessCode !== 'DESIGN_RESOURCE_UPDATED' ||
            !isStudentReadNotificationPage(response.data, notificationId)
          ) {
            this.actionError.set('Chưa thể cập nhật trạng thái thông báo. Vui lòng thử lại.');
            this.reloadAfterMutation();
            return;
          }
          this.actionMessage.set('Thông báo đã được đánh dấu đã đọc.');
          this.reloadAfterMutation();
        },
        error: (error: unknown) => {
          this.markingId.set(null);
          this.actionError.set(studentApiErrorMessage(error));
          this.reloadAfterMutation();
        },
      });
  }

  markAllRead(): void {
    const unreadCount = this.unreadCount();
    if (
      this.loading() ||
      this.loadingUnreadCount() ||
      unreadCount === null ||
      unreadCount === 0 ||
      this.markingAll() ||
      this.markingId() !== null
    ) {
      return;
    }

    this.markingAll.set(true);
    this.actionError.set(null);
    this.actionMessage.set(null);
    this.data
      .markAllRead()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          this.markingAll.set(false);
          if (
            !response.success ||
            response.businessCode !== 'DESIGN_RESOURCE_UPDATED' ||
            !isStudentNotificationReadSummary(response.data)
          ) {
            this.actionError.set('Chưa thể cập nhật thông báo. Vui lòng thử lại.');
            this.reloadAfterMutation();
            return;
          }
          this.actionMessage.set(
            response.data.updated_count === 0
              ? 'Không có thông báo chưa đọc cần đánh dấu.'
              : `${response.data.updated_count} thông báo đã được đánh dấu đã đọc.`,
          );
          this.reloadAfterMutation();
        },
        error: (error: unknown) => {
          this.markingAll.set(false);
          this.actionError.set(studentApiErrorMessage(error));
          this.reloadAfterMutation();
        },
      });
  }

  private reloadAfterMutation(): void {
    this.load();
    this.refreshUnreadCount();
  }

  private applyListResult(result: NotificationListResult): void {
    this.loading.set(false);
    if (result.error !== null) {
      this.error.set(studentApiErrorMessage(result.error));
      return;
    }
    const response = result.response;
    if (!response?.success) {
      this.error.set('Chưa thể tải danh sách thông báo. Vui lòng thử lại.');
      return;
    }
    if (
      response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isStudentNotificationPage(response.data, result.request.page, 20, result.request.unreadOnly)
    ) {
      this.error.set('Danh sách thông báo chưa đúng định dạng. Hãy tải lại trang.');
      return;
    }
    const lastPage = Math.max(1, response.data.pagination.total_pages);
    if (result.request.page > lastPage) {
      this.page.set(lastPage);
      this.listRequests$.next({ ...result.request, page: lastPage });
      return;
    }
    // COUNT và LIST chạy riêng, nên tránh nhầm race dữ liệu với danh sách rỗng hợp lệ.
    if (response.data.items.length === 0 && response.data.pagination.total > 0) {
      if (result.request.page > 1) {
        const previousPage = result.request.page - 1;
        this.page.set(previousPage);
        this.listRequests$.next({ ...result.request, page: previousPage });
        return;
      }
      this.error.set('Danh sách thông báo vừa thay đổi. Vui lòng tải lại.');
      return;
    }
    if (!result.request.unreadOnly) {
      this.allCount.set(response.data.pagination.total);
    }
    this.notifications.set(response.data.items);
    this.pagination.set(response.data.pagination);
  }

  private applyUnreadCountResult(result: UnreadCountResult): void {
    this.loadingUnreadCount.set(false);
    if (result.error !== null) {
      this.unreadCount.set(null);
      this.unreadCountError.set(studentApiErrorMessage(result.error));
      return;
    }
    const response = result.response;
    if (
      !response?.success ||
      response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isStudentNotificationPage(response.data, 1, 20, true)
    ) {
      this.unreadCount.set(null);
      this.unreadCountError.set(
        'Chưa thể xác định tổng số thông báo chưa đọc. Vui lòng thử lại.',
      );
      return;
    }
    this.unreadCount.set(response.data.pagination.total);
  }
}

interface NotificationRequest {
  unreadOnly: boolean;
  page: number;
}

interface NotificationDateGroup {
  key: string;
  label: string;
  items: StudentNotification[];
}

interface NotificationListResult {
  request: NotificationRequest;
  response: ApiEnvelope<StudentPage<StudentNotification>> | null;
  error: unknown | null;
}

interface UnreadCountResult {
  response: ApiEnvelope<StudentPage<StudentNotification>> | null;
  error: unknown | null;
}

function localDateKey(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function dateGroupKey(date: Date): string {
  return Number.isNaN(date.getTime()) ? 'unknown-date' : localDateKey(date);
}

function dateGroupLabel(
  key: string,
  date: Date,
  todayKey: string,
  yesterdayKey: string,
  formatter: Intl.DateTimeFormat,
): string {
  if (key === 'unknown-date') return 'Thời gian không xác định';
  if (key === todayKey) return 'Hôm nay';
  if (key === yesterdayKey) return 'Hôm qua';
  return formatter.format(date);
}
