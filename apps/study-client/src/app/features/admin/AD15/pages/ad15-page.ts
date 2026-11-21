import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { AD15ApiService } from '../data-access/ad15-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD15_SCREEN } from '../models/ad15-screen.model';
import { adminQueryState, loadedRows } from '../../admin-screen-state';
import { hasAdminPageCountMismatch, isAdminQuizPage } from '../../admin-api-guards';
import { renderQuizRow } from '../../admin-screen-renderers';

interface AD15Query {
  course?: string;
  status?: string;
  page: number;
}

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad15-page',
  templateUrl: './ad15-page.html',
})
export class AD15Page {
  readonly definition = AD15_SCREEN;
  private readonly api = inject(AD15ApiService);
  readonly filterCourse = signal('');
  readonly filterStatus = signal('');
  readonly query = signal<AD15Query>({ page: 1 });
  readonly snapshotMismatch = signal(false);
  readonly pageOutOfRange = signal(false);
  readonly viewState = adminQueryState(
    this.query,
    (query) => this.api.getQuizzes(query),
    (page) => {
      if (!isAdminQuizPage(page, this.query().page)) {
        this.clearPageFlags();
        return { status: 'error', message: 'API #87 trả về trang bài kiểm tra không hợp lệ.' };
      }

      const isOutOfRange = page.items.length === 0
        && page.pagination.page > Math.max(page.pagination.total_pages, 1);
      this.pageOutOfRange.set(isOutOfRange);
      this.snapshotMismatch.set(!isOutOfRange && hasAdminPageCountMismatch(page));
      return loadedRows(page.items.map(renderQuizRow), {
        page: page.pagination.page,
        total: page.pagination.total,
        totalPages: page.pagination.total_pages,
        size: page.pagination.size,
      });
    },
    'DESIGN_RESOURCE_RETRIEVED',
  );

  setFilterCourse(value: string): void {
    this.filterCourse.set(value);
  }

  setFilterStatus(value: string): void {
    this.filterStatus.set(value);
  }

  applyFilters(filters: Readonly<Record<string, string>>): void {
    this.clearPageFlags();
    this.query.set({
      course: filters['course'] || undefined,
      status: filters['status'] || undefined,
      page: 1,
    });
  }

  submitFilters(event: Event): void {
    event.preventDefault();
    this.applyFilters({ course: this.filterCourse(), status: this.filterStatus() });
  }

  clearFilters(): void {
    this.clearPageFlags();
    this.filterCourse.set('');
    this.filterStatus.set('');
    this.query.set({ page: 1 });
  }

  refreshQuizzes(): void {
    this.clearPageFlags();
    this.query.update((query) => ({ ...query }));
  }

  changePage(page: number): void {
    if (this.snapshotMismatch() || this.pageOutOfRange()) return;
    const pagination = this.viewState().pagination;
    if (pagination && Number.isSafeInteger(page) && page >= 1 && page <= pagination.totalPages) {
      this.clearPageFlags();
      this.query.update((query) => ({ ...query, page }));
    }
  }

  returnToFirstPage(): void {
    if (!this.pageOutOfRange() && !this.snapshotMismatch()) return;
    this.clearPageFlags();
    this.query.update((query) => ({ ...query, page: 1 }));
  }

  private clearPageFlags(): void {
    this.snapshotMismatch.set(false);
    this.pageOutOfRange.set(false);
  }

  quizDeleteRoute(statisticsRoute: string | undefined): string | null {
    const match = /^\/admin\/quizzes\/([1-9][0-9]*)\/statistics$/.exec(statisticsRoute ?? '');
    const quizId = match?.[1];
    if (!quizId) {
      return null;
    }

    const numericId = Number(quizId);
    if (!Number.isSafeInteger(numericId) || numericId <= 0 || String(numericId) !== quizId) {
      return null;
    }

    return `/admin/quizzes/${quizId}/delete`;
  }
}
