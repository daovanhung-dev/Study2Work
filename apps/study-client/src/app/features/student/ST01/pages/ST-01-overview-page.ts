import { StudentOverviewService } from '../data-access/ST-01-overview.service';
import type { Achievement, EnrolledCourse, OverviewWidget, OverviewWidgetKey, StudentNotification } from '../models/ST-01-overview.models';
import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ChangeDetectionStrategy, Component, DestroyRef, OnInit, computed, inject, signal } from '@angular/core';
import { StudentOverviewView } from '../ui/ST-01-overview-view';

@Component({
  selector: 'study-student-overview-page',
  imports: [StudentOverviewView],
  templateUrl: './ST-01-overview-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentOverviewPage implements OnInit {
  private readonly source = inject(StudentOverviewService);
  private readonly destroyRef = inject(DestroyRef);

  readonly courses = signal<OverviewWidget<EnrolledCourse>>({ kind: 'loading' });
  readonly progress = signal<OverviewWidget<never>>({ kind: 'loading' });
  readonly achievements = signal<OverviewWidget<Achievement>>({ kind: 'loading' });
  readonly notifications = signal<OverviewWidget<StudentNotification>>({ kind: 'loading' });
  readonly statusLabel = computed(() => {
    const widgets = [this.courses(), this.progress(), this.achievements(), this.notifications()];
    if (widgets.some((widget) => widget.kind === 'loading')) return 'Đang tải dữ liệu';
    if (widgets.some((widget) => widget.kind === 'error')) return 'Một số nguồn gặp lỗi';
    if (this.progress().kind === 'contract-gap') return 'Tiến độ chờ dữ liệu từ API #21';
    return 'Dữ liệu đã được kiểm tra';
  });

  ngOnInit(): void {
    this.load('courses');
    this.load('progress');
    this.load('achievements');
    this.load('notifications');
  }

  load(widget: OverviewWidgetKey): void {
    switch (widget) {
      case 'courses':
        this.courses.set({ kind: 'loading' });
        this.source.getCourses().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
          next: ({ items, total }) => this.courses.set(items.length ? { kind: 'ready', items, total } : { kind: 'empty' }),
          error: (error: unknown) => this.courses.set(toErrorState(error)),
        });
        break;
      case 'progress':
        this.progress.set({ kind: 'loading' });
        this.source.getProgressContract().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
          next: (message) => this.progress.set({ kind: 'contract-gap', message }),
          error: (error: unknown) => this.progress.set(toErrorState(error)),
        });
        break;
      case 'achievements':
        this.achievements.set({ kind: 'loading' });
        this.source.getAchievements().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
          next: ({ items, total }) => this.achievements.set(items.length ? { kind: 'ready', items, total } : { kind: 'empty' }),
          error: (error: unknown) => this.achievements.set(toErrorState(error)),
        });
        break;
      case 'notifications':
        this.notifications.set({ kind: 'loading' });
        this.source.getNotifications().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
          next: ({ items, total }) => this.notifications.set(items.length ? { kind: 'ready', items, total } : { kind: 'empty' }),
          error: (error: unknown) => this.notifications.set(toErrorState(error)),
        });
    }
  }
}

function toErrorState(error: unknown): OverviewWidget<never> {
  const http = error instanceof HttpErrorResponse ? error : null;
  const body = http?.error && typeof http.error === 'object' ? http.error as Record<string, unknown> : {};
  const trace = body['traceId'] ?? http?.headers.get('X-Trace-Id');
  const message = http?.status === 401 || http?.status === 403
    ? 'Phiên đăng nhập hoặc quyền truy cập không hợp lệ.'
    : http?.status ? `Máy chủ trả HTTP ${http.status}. Vui lòng thử lại.` : 'Không đọc được phản hồi hợp lệ từ máy chủ.';
  return { kind: 'error', message, traceId: typeof trace === 'string' ? trace : undefined };
}
