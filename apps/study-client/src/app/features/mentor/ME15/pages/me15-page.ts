import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, computed, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Me15NotificationStatusService } from '../data-access/me15-notification-status.service';
import {
  computeNotificationSummary,
  NotificationStatusItemVm,
  parseNotificationIds,
} from '../models/me15-notification-status.models';
import { Me15StatusSummaryComponent } from '../ui/me15-status-summary';
import { Me15StatusTableComponent } from '../ui/me15-status-table';

@Component({
  selector: 'app-me15-page',
  imports: [FormsModule, Me15StatusSummaryComponent, Me15StatusTableComponent],
  templateUrl: './me15-page.html',
  styleUrl: './me15-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ME15Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly service = inject(Me15NotificationStatusService);

  readonly lookupInput = signal<string>('');
  readonly trackedIds = signal<number[]>([]);
  readonly items = signal<NotificationStatusItemVm[]>([]);
  readonly loading = signal<boolean>(false);
  readonly errorCode = signal<string | null>(null);
  readonly errorMessage = signal<string | null>(null);

  readonly summary = computed(() => computeNotificationSummary(this.items()));

  ngOnInit(): void {
    const paramId = this.route.snapshot.paramMap.get('notificationId');
    const queryIds = this.route.snapshot.queryParamMap.get('ids');
    const ids = parseNotificationIds(paramId, queryIds);

    if (paramId && ids.length === 0) {
      this.errorCode.set('INVALID_NOTIFICATION_ID');
      this.errorMessage.set('Mã thông báo trên đường dẫn không hợp lệ (cần số nguyên dương).');
      return;
    }

    if (ids.length > 0) {
      this.trackedIds.set(ids);
      this.lookupInput.set(ids.join(','));
      this.refreshStatuses();
    }
  }

  onLookupSubmit(): void {
    const ids = parseNotificationIds(null, this.lookupInput());
    if (ids.length === 0) {
      this.errorCode.set('INVALID_NOTIFICATION_ID');
      this.errorMessage.set('Vui lòng nhập ít nhất một mã thông báo nguyên dương (ví dụ: 900, 901).');
      return;
    }
    this.trackedIds.set(ids);
    this.refreshStatuses();
  }

  refreshStatuses(): void {
    const ids = this.trackedIds();
    if (ids.length === 0) {
      return;
    }
    this.loading.set(true);
    this.errorCode.set(null);
    this.errorMessage.set(null);

    this.service.getBatchStatuses(ids).subscribe({
      next: (results) => {
        this.items.set(results);
        this.loading.set(false);
      },
      error: (err: unknown) => {
        this.loading.set(false);
        if (err instanceof HttpErrorResponse) {
          const apiCode =
            (err.error as { error?: { code?: string } } | null)?.error?.code ??
            `HTTP_${err.status}`;
          const apiMsg =
            (err.error as { error?: { message?: string } } | null)?.error?.message ?? err.message;
          this.errorCode.set(apiCode);
          this.errorMessage.set(apiMsg);
        } else {
          this.errorCode.set('UNKNOWN_ERROR');
          this.errorMessage.set('Không thể tải trạng thái gửi thông báo.');
        }
      },
    });
  }

  startNewNotification(): void {
    const courseId = this.route.snapshot.queryParamMap.get('courseId');
    void this.router.navigate(['/mentor/notifications/recipients'], {
      queryParams: courseId ? { courseId } : undefined,
    });
  }
}
