import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { Me09SubmissionsService } from '../data-access/me09-submissions.service';
import {
  type MentorCourseOptionDto,
  type SubmissionItemDto,
  type SubmissionPaginationDto,
  parsePositiveInt32,
  parsePositiveInt64,
} from '../models/me09-submissions.models';
import { Me09FilterBar } from '../ui/me09-filter-bar';
import { Me09Header } from '../ui/me09-header';
import { Me09SubmissionList } from '../ui/me09-submission-list';

export type Me09ScreenState =
  | 'loading'
  | 'empty'
  | 'ready'
  | 'unauthorized'
  | 'forbidden'
  | 'validation-error'
  | 'error';

@Component({
  imports: [Me09Header, Me09FilterBar, Me09SubmissionList],
  selector: 'study-me09-page',
  styleUrl: './me09-page.css',
  templateUrl: './me09-page.html',
})
export class ME09Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly submissionsService = inject(Me09SubmissionsService);

  readonly screenState = signal<Me09ScreenState>('loading');
  readonly errorMessage = signal<string>('');
  readonly traceId = signal<string>('');

  readonly courses = signal<readonly MentorCourseOptionDto[]>([]);
  readonly coursesLoading = signal<boolean>(false);

  readonly selectedCourseId = signal<number | null>(null);
  readonly selectedStatus = signal<string>('');
  readonly currentPage = signal<number>(1);

  readonly items = signal<readonly SubmissionItemDto[]>([]);
  readonly pagination = signal<SubmissionPaginationDto>({
    page: 1,
    size: 20,
    total: 0,
    total_pages: 0,
  });

  ngOnInit(): void {
    const queryMap = this.route.snapshot.queryParamMap;
    const rawCourseId = queryMap.get('courseId') ?? queryMap.get('course_id');
    const rawStatus = queryMap.get('status') ?? '';
    const rawPage = queryMap.get('page');

    this.selectedCourseId.set(parsePositiveInt64(rawCourseId));
    this.selectedStatus.set(rawStatus.trim());
    this.currentPage.set(parsePositiveInt32(rawPage, 1));

    this.loadMentorCourses();
    this.loadSubmissions();
  }

  onCourseFilterChange(courseId: number | null): void {
    this.selectedCourseId.set(courseId);
    this.currentPage.set(1);
    this.loadSubmissions();
  }

  onStatusFilterChange(status: string): void {
    this.selectedStatus.set(status.trim());
    this.currentPage.set(1);
    this.loadSubmissions();
  }

  onPageChange(nextPage: number): void {
    if (nextPage < 1) {
      return;
    }
    this.currentPage.set(nextPage);
    this.loadSubmissions();
  }

  resetFilters(): void {
    this.selectedCourseId.set(null);
    this.selectedStatus.set('');
    this.currentPage.set(1);
    this.loadSubmissions();
  }

  refreshList(): void {
    this.loadSubmissions();
  }

  openSubmissionDetail(submissionId: number): void {
    void this.router.navigate(['/mentor/submissions', submissionId]);
  }

  private loadMentorCourses(): void {
    this.coursesLoading.set(true);
    this.submissionsService.getMentorCourses().subscribe({
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

  private loadSubmissions(): void {
    this.screenState.set('loading');
    this.errorMessage.set('');
    this.traceId.set('');

    this.submissionsService
      .getSubmissions({
        course_id: this.selectedCourseId(),
        status: this.selectedStatus() || null,
        page: this.currentPage(),
      })
      .subscribe({
        next: (envelope) => {
          const pageData = envelope.data;
          const list = Array.isArray(pageData?.items) ? pageData.items : [];
          this.items.set(list);
          this.pagination.set(
            pageData?.pagination ?? {
              page: this.currentPage(),
              size: 20,
              total: list.length,
              total_pages: list.length > 0 ? 1 : 0,
            },
          );
          this.traceId.set(envelope.traceId ?? '');
          this.screenState.set(list.length === 0 ? 'empty' : 'ready');
        },
        error: (err: unknown) => {
          this.items.set([]);
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
                'Bạn không có quyền truy cập danh sách bài nộp của khóa học này (403).',
              );
              return;
            }
            if (err.status === 422) {
              this.screenState.set('validation-error');
              this.errorMessage.set(
                body?.message ?? 'Tham số lọc bài nộp không hợp lệ (422).',
              );
              return;
            }
            this.errorMessage.set(
              body?.message ?? 'Không thể tải danh sách bài nộp cần chấm.',
            );
          } else {
            this.errorMessage.set('Lỗi kết nối tới máy chủ Study API.');
          }
          this.screenState.set('error');
        },
      });
  }
}
