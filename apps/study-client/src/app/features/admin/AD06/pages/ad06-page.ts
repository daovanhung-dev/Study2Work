import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { AD06ApiService } from '../data-access/ad06-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD06_SCREEN } from '../models/ad06-screen.model';
import { adminQueryState, loadedRows } from '../../admin-screen-state';
import { hasAdminPageCountMismatch, isAdminCoursePage } from '../../admin-api-guards';
import { renderCourseRow } from '../../admin-screen-renderers';

interface AD06Query {
  page: number;
}

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad06-page',
  templateUrl: './ad06-page.html',
})
export class AD06Page {
  readonly definition = AD06_SCREEN;
  private readonly api = inject(AD06ApiService);
  readonly query = signal<AD06Query>({ page: 1 });
  readonly snapshotMismatch = signal(false);
  readonly viewState = adminQueryState(
    this.query,
    (query) => this.api.getCourses(query),
    (page) => {
      if (!isAdminCoursePage(page, this.query().page)) {
        this.snapshotMismatch.set(false);
        return { status: 'error', message: 'API #73 trả về trang khóa học không hợp lệ.' };
      }

      this.snapshotMismatch.set(hasAdminPageCountMismatch(page));
      return loadedRows(page.items.map(renderCourseRow), {
        page: page.pagination.page,
        total: page.pagination.total,
        totalPages: page.pagination.total_pages,
        size: page.pagination.size,
      });
    },
    'DESIGN_RESOURCE_RETRIEVED',
  );

  get totalCount(): string {
    if (this.snapshotMismatch() || this.isOutOfRange) return '—';
    const total = this.viewState().pagination?.total;
    if (total === undefined) {
      return '—';
    }
    return Number.isSafeInteger(total) && total >= 0
      ? total.toLocaleString('vi-VN')
      : 'Không thể hiển thị chính xác';
  }

  get pageCount(): string {
    if (this.snapshotMismatch() || this.isOutOfRange) return '—';
    const pagination = this.viewState().pagination;
    if (!pagination || pagination.totalPages <= 0) {
      return '—';
    }
    if (!Number.isSafeInteger(pagination.page) || pagination.page < 1) {
      return 'Không thể hiển thị chính xác';
    }
    return Number.isSafeInteger(pagination.totalPages)
      ? `${pagination.page} / ${pagination.totalPages}`
      : `${pagination.page} / Không thể hiển thị chính xác`;
  }

  get currentResultCount(): string {
    return this.viewState().status === 'loaded'
      ? String(this.viewState().rows?.length ?? 0)
      : '—';
  }

  get pageSize(): string {
    const pagination = this.viewState().pagination;
    return pagination ? String(pagination.size ?? '—') : '—';
  }

  get isOutOfRange(): boolean {
    const state = this.viewState();
    const pagination = state.pagination;
    return state.status === 'loaded'
      && (state.rows?.length ?? 0) === 0
      && !!pagination
      && Number.isSafeInteger(pagination.total)
      && pagination.page > Math.max(pagination.totalPages, 1);
  }

  get isEmpty(): boolean {
    const state = this.viewState();
    return state.status === 'loaded'
      && !this.snapshotMismatch()
      && !this.isOutOfRange
      && (state.rows?.length ?? 0) === 0
      && (state.pagination?.total ?? 0) === 0;
  }

  get previousDisabled(): boolean {
    const state = this.viewState();
    return this.snapshotMismatch() || this.isOutOfRange
      || state.status !== 'loaded' || !state.pagination || state.pagination.page <= 1;
  }

  get nextDisabled(): boolean {
    const state = this.viewState();
    return this.snapshotMismatch() || this.isOutOfRange
      || state.status !== 'loaded' || !state.pagination
      || state.pagination.totalPages === 0
      || state.pagination.page >= state.pagination.totalPages;
  }

  changePage(page: number): void {
    if (this.snapshotMismatch() || this.isOutOfRange) return;
    const pagination = this.viewState().pagination;
    if (this.viewState().status !== 'loaded' || !pagination || !Number.isSafeInteger(page)
      || page < 1 || page > pagination.totalPages) {
      return;
    }
    this.snapshotMismatch.set(false);
    this.query.set({ page });
  }

  refreshCourses(): void {
    this.snapshotMismatch.set(false);
    this.query.update((query) => ({ ...query }));
  }

  returnToFirstPage(): void {
    if (!this.isOutOfRange) return;
    this.snapshotMismatch.set(false);
    this.query.set({ page: 1 });
  }
}
