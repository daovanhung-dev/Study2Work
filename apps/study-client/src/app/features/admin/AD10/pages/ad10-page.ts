import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { AD10ApiService } from '../data-access/ad10-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD10_SCREEN } from '../models/ad10-screen.model';
import { adminQueryState, loadedRows } from '../../admin-screen-state';
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
  readonly viewState = adminQueryState(
    this.query,
    (query) => this.api.getPendingContent(query),
    (page) => loadedRows(page.items.map(renderContentRow), {
      page: page.pagination.page,
      total: page.pagination.total,
      totalPages: page.pagination.total_pages,
    }),
  );

  setFilterType(value: string): void {
    this.filterType.set(value);
  }

  setFilterCourse(value: string): void {
    this.filterCourse.set(value);
  }

  applyFilters(filters: Readonly<Record<string, string>>): void {
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
    this.filterType.set('');
    this.filterCourse.set('');
    this.query.set({ page: 1 });
  }

  changePage(page: number): void {
    const pagination = this.viewState().pagination;
    if (pagination && Number.isSafeInteger(page) && page >= 1 && page <= pagination.totalPages) {
      this.query.update((query) => ({ ...query, page }));
    }
  }
}
