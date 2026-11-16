import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { AD06ApiService } from '../data-access/ad06-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD06_SCREEN } from '../models/ad06-screen.model';
import { adminQueryState, loadedRows } from '../../admin-screen-state';
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
  readonly viewState = adminQueryState(
    this.query,
    (query) => this.api.getCourses(query),
    (page) => loadedRows(page.items.map(renderCourseRow), {
      page: page.pagination.page,
      total: page.pagination.total,
      totalPages: page.pagination.total_pages,
      size: page.pagination.size,
    }),
  );

  get totalCount(): string {
    const pagination = this.viewState().pagination;
    return pagination ? pagination.total.toLocaleString('vi-VN') : '—';
  }

  get pageCount(): string {
    const pagination = this.viewState().pagination;
    return pagination && pagination.totalPages > 0
      ? `${pagination.page} / ${pagination.totalPages}`
      : '—';
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
    return state.status === 'loaded'
      && (state.rows?.length ?? 0) === 0
      && (state.pagination?.total ?? 0) > 0;
  }

  get isEmpty(): boolean {
    const state = this.viewState();
    return state.status === 'loaded'
      && (state.rows?.length ?? 0) === 0
      && (state.pagination?.total ?? 0) === 0;
  }

  get previousDisabled(): boolean {
    const state = this.viewState();
    return state.status !== 'loaded' || !state.pagination || state.pagination.page <= 1;
  }

  get nextDisabled(): boolean {
    const state = this.viewState();
    return state.status !== 'loaded' || !state.pagination
      || state.pagination.totalPages === 0
      || state.pagination.page >= state.pagination.totalPages;
  }

  changePage(page: number): void {
    const pagination = this.viewState().pagination;
    if (this.viewState().status !== 'loaded' || !pagination || page < 1 || page > pagination.totalPages) {
      return;
    }
    this.query.set({ page });
  }
}
