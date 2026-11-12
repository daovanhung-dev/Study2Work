import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { Me11SupportService } from '../data-access/me11-support.service';
import {
  type Me11CourseOptionDto,
  type SupportRequestItemDto,
  type SupportStatusCountsVm,
  computeSupportCounts,
  parsePositiveInt64,
} from '../models/me11-support.models';
import { Me11FilterBar } from '../ui/me11-filter-bar';
import { Me11RequestList } from '../ui/me11-request-list';

export type Me11ScreenState =
  | 'loading'
  | 'empty'
  | 'ready'
  | 'unauthorized'
  | 'forbidden'
  | 'validation-error'
  | 'error';

@Component({
  imports: [Me11FilterBar, Me11RequestList],
  selector: 'study-me11-page',
  styleUrl: './me11-page.css',
  templateUrl: './me11-page.html',
})
export class ME11Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly supportService = inject(Me11SupportService);

  readonly screenState = signal<Me11ScreenState>('loading');
  readonly errorMessage = signal<string>('');
  readonly traceId = signal<string>('');

  readonly courses = signal<readonly Me11CourseOptionDto[]>([]);
  readonly coursesLoading = signal<boolean>(false);

  readonly selectedCourseId = signal<number | null>(null);
  readonly selectedStatus = signal<string>('');

  readonly requests = signal<readonly SupportRequestItemDto[]>([]);
  readonly counts = computed<SupportStatusCountsVm>(() => computeSupportCounts(this.requests()));

  ngOnInit(): void {
    const queryMap = this.route.snapshot.queryParamMap;
    const rawCourseId = queryMap.get('courseId') ?? queryMap.get('course_id');
    const rawStatus = queryMap.get('status') ?? '';

    this.selectedCourseId.set(parsePositiveInt64(rawCourseId));
    this.selectedStatus.set(rawStatus.trim());

    this.loadMentorCourses();
    this.loadSupportInbox();
  }

  onStatusChange(status: string): void {
    this.selectedStatus.set(status.trim());
    this.loadSupportInbox();
  }

  onCourseChange(courseId: number | null): void {
    this.selectedCourseId.set(courseId);
    this.loadSupportInbox();
  }

  refreshInbox(): void {
    this.loadSupportInbox();
  }

  openSupportThread(requestId: number): void {
    void this.router.navigate(['/mentor/support', requestId]);
  }

  private loadMentorCourses(): void {
    this.coursesLoading.set(true);
    this.supportService.getMentorCourses().subscribe({
      next: (envelope) => {
        this.courses.set(envelope.data?.items ?? []);
        this.coursesLoading.set(false);
      },
      error: () => {
        this.courses.set([]);
        this.coursesLoading.set(false);
      },
    });
  }

  private loadSupportInbox(): void {
    this.screenState.set('loading');
    this.errorMessage.set('');
    this.traceId.set('');

    this.supportService
      .getSupportRequests({
        course_id: this.selectedCourseId(),
        status: this.selectedStatus() || null,
      })
      .subscribe({
        next: (envelope) => {
          const list = Array.isArray(envelope.data) ? envelope.data : [];
          this.requests.set(list);
          this.traceId.set(envelope.traceId ?? '');
          this.screenState.set(list.length === 0 ? 'empty' : 'ready');
        },
        error: (err: unknown) => {
          this.requests.set([]);
          if (err instanceof HttpErrorResponse) {
            const body = err.error as { message?: string; traceId?: string } | null;
            this.traceId.set(body?.traceId ?? '');
            if (err.status === 401) {
              this.screenState.set('unauthorized');
              this.errorMessage.set(
                'Phiên đăng nhập giảng viên chưa xác thực hoặc đã hết hạn (401).',
              );
              return;
            }
            if (err.status === 403) {
              this.screenState.set('forbidden');
              this.errorMessage.set(
                'Bạn không có quyền truy cập hộp thư hỗ trợ của khóa học này (403).',
              );
              return;
            }
            if (err.status === 422) {
              this.screenState.set('validation-error');
              this.errorMessage.set(
                body?.message ?? 'Tham số lọc yêu cầu hỗ trợ không hợp lệ (422).',
              );
              return;
            }
            this.errorMessage.set(
              body?.message ?? 'Không thể tải danh sách yêu cầu hỗ trợ học viên.',
            );
          } else {
            this.errorMessage.set('Lỗi kết nối tới máy chủ Study API.');
          }
          this.screenState.set('error');
        },
      });
  }
}
