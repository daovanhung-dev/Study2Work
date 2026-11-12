import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { Me16ProgressService } from '../data-access/me16-progress.service';
import {
  type Me16RosterKpiVm,
  type MentorStudentProgressDto,
  computeRosterKpi,
  parseCourseIdParam,
} from '../models/me16-progress.models';
import { Me16RosterTable } from '../ui/me16-roster-table';
import { Me16SummaryStrip } from '../ui/me16-summary-strip';

export type Me16ScreenState =
  | 'invalid-param'
  | 'loading'
  | 'empty'
  | 'ready'
  | 'unauthorized'
  | 'forbidden'
  | 'not-found'
  | 'error';

@Component({
  imports: [RouterLink, Me16SummaryStrip, Me16RosterTable],
  selector: 'study-me16-page',
  styleUrl: './me16-page.css',
  templateUrl: './me16-page.html',
})
export class ME16Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly progressService = inject(Me16ProgressService);

  readonly courseId = signal<number | null>(null);
  readonly screenState = signal<Me16ScreenState>('loading');
  readonly errorMessage = signal<string>('');
  readonly traceId = signal<string>('');

  readonly items = signal<readonly MentorStudentProgressDto[]>([]);
  readonly searchKeyword = signal<string>('');

  readonly kpi = computed<Me16RosterKpiVm>(() => computeRosterKpi(this.items()));
  readonly filteredItems = computed<readonly MentorStudentProgressDto[]>(() => {
    const kw = this.searchKeyword().trim().toLowerCase();
    if (!kw) {
      return this.items();
    }
    return this.items().filter(
      (row) =>
        row.student.full_name.toLowerCase().includes(kw) ||
        String(row.student.id).includes(kw),
    );
  });

  ngOnInit(): void {
    const rawCourseId = this.route.snapshot.paramMap.get('courseId');
    const parsed = parseCourseIdParam(rawCourseId);
    if (parsed === null) {
      this.courseId.set(null);
      this.screenState.set('invalid-param');
      this.errorMessage.set('Mã khóa học trên đường dẫn không phải số nguyên dương int64 hợp lệ.');
      return;
    }

    this.courseId.set(parsed);
    this.loadProgress(parsed);
  }

  onSearchInput(event: Event): void {
    const val = (event.target as HTMLInputElement | null)?.value ?? '';
    this.searchKeyword.set(val);
  }

  reloadProgress(): void {
    const id = this.courseId();
    if (id !== null) {
      this.loadProgress(id);
    }
  }

  openStudentDetail(studentId: number): void {
    const id = this.courseId();
    if (id === null) {
      return;
    }
    void this.router.navigate(['/mentor/courses', id, 'students', studentId, 'progress']);
  }

  openCourseAnalytics(): void {
    const id = this.courseId();
    if (id === null) {
      return;
    }
    void this.router.navigate(['/mentor/courses', id, 'analytics']);
  }

  private loadProgress(courseId: number): void {
    this.screenState.set('loading');
    this.errorMessage.set('');
    this.traceId.set('');

    this.progressService.getCourseProgress(courseId).subscribe({
      next: (envelope) => {
        const list = Array.isArray(envelope.data?.items) ? envelope.data.items : [];
        this.items.set(list);
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
            this.errorMessage.set('Phiên đăng nhập giảng viên chưa xác thực hoặc đã hết hạn (401).');
            return;
          }
          if (err.status === 403) {
            this.screenState.set('forbidden');
            this.errorMessage.set('Bạn không có quyền truy cập tiến độ của khóa học này (403).');
            return;
          }
          if (err.status === 404) {
            this.screenState.set('not-found');
            this.errorMessage.set('Không tìm thấy khóa học theo mã đã cung cấp (404).');
            return;
          }
          this.errorMessage.set(body?.message ?? 'Không thể tải tiến độ toàn khóa học.');
        } else {
          this.errorMessage.set('Lỗi kết nối tới máy chủ Study API.');
        }
        this.screenState.set('error');
      },
    });
  }
}
