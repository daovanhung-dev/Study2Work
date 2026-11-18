import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import type { Subscription } from 'rxjs';

import { StudentCoursesService } from '../data-access/ST-08-courses.service';
import type { StudentCoursesState } from '../models/ST-08-courses.models';
import { StudentCoursesView } from '../ui/ST-08-courses-view';

@Component({
  selector: 'study-student-courses-page',
  imports: [StudentCoursesView],
  templateUrl: './ST-08-courses-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentCoursesPage implements OnInit {
  private readonly source = inject(StudentCoursesService);
  private readonly destroyRef = inject(DestroyRef);
  private request?: Subscription;
  private currentPage = 1;

  readonly state = signal<StudentCoursesState>({ kind: 'loading' });

  ngOnInit(): void {
    this.load(1);
  }

  load(page: number): void {
    if (!Number.isSafeInteger(page) || page < 1) return;
    this.request?.unsubscribe();
    this.currentPage = page;
    this.state.set({ kind: 'loading' });
    this.request = this.source.getCourses(page).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (result) => this.state.set(
        result.items.length === 0 && result.pagination.total === 0
          ? { kind: 'empty' }
          : { kind: 'ready', page: result },
      ),
      error: (error: unknown) => this.state.set(toErrorState(error)),
    });
  }

  retry(): void {
    this.load(this.currentPage);
  }
}

function toErrorState(error: unknown): StudentCoursesState {
  const http = error instanceof HttpErrorResponse ? error : null;
  const body = http?.error && typeof http.error === 'object' ? http.error as Record<string, unknown> : null;
  const trace = body?.['traceId'] ?? http?.headers.get('X-Trace-Id');
  return {
    kind: 'error',
    message: http?.status ? `Máy chủ trả HTTP ${http.status}. Vui lòng thử lại.` : 'Không đọc được danh sách khóa học hợp lệ. Vui lòng thử lại.',
    ...(typeof trace === 'string' ? { traceId: trace } : {}),
  };
}
