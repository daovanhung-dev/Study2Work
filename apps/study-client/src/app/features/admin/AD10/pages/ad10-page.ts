import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { AD10ApiService } from '../data-access/ad10-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD10_SCREEN } from '../models/ad10-screen.model';
import { adminQueryState, loadedRows } from '../../admin-screen-state';
import { hasAdminPageCountMismatch, isAdminContentPage } from '../../admin-api-guards';
import { renderContentRow } from '../../admin-screen-renderers';

interface AD10Query {
  type?: string;
  course?: string;
  page: number;
}

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad10-page',
  templateUrl: './ad10-page.html',
})
export class AD10Page {
  readonly definition = AD10_SCREEN;
  private readonly api = inject(AD10ApiService);
  readonly filterType = signal('');
  readonly filterCourse = signal('');
  readonly query = signal<AD10Query>({ page: 1 });
  readonly snapshotMismatch = signal(false);
  readonly pageOutOfRange = signal(false);
  readonly viewState = adminQueryState(
    this.query,
    (query) => this.api.getPendingContent(query),
    (page) => {
      if (!isAdminContentPage(page, this.query().page)) {
        this.clearPageFlags();
        return { status: 'error', message: 'API #78 trả về trang nội dung không hợp lệ.' };
      }

      const isOutOfRange = page.items.length === 0
        && page.pagination.page > Math.max(page.pagination.total_pages, 1);
      this.pageOutOfRange.set(isOutOfRange);
      this.snapshotMismatch.set(!isOutOfRange && hasAdminPageCountMismatch(page));
      return loadedRows(page.items.map(renderContentRow), {
        page: page.pagination.page,
        total: page.pagination.total,
        totalPages: page.pagination.total_pages,
        size: page.pagination.size,
      });
    },
    'DESIGN_RESOURCE_RETRIEVED',
  );

  setFilterType(value: string): void {
    this.filterType.set(value);
  }

  setFilterCourse(value: string): void {
    this.filterCourse.set(value);
  }

  applyFilters(filters: Readonly<Record<string, string>>): void {
    this.clearPageFlags();
    this.query.set({
      type: filters['type'] || undefined,
      course: filters['course'] || undefined,
      page: 1,
    });
  }

  submitFilters(event: Event): void {
    event.preventDefault();
    this.applyFilters({ type: this.filterType(), course: this.filterCourse() });
  }

  clearFilters(): void {
    this.clearPageFlags();
    this.filterType.set('');
    this.filterCourse.set('');
    this.query.set({ page: 1 });
  }

  refreshQueue(): void {
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
}
