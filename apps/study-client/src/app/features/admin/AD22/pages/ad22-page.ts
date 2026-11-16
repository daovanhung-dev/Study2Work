import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { AD22ApiService } from '../data-access/ad22-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD22_SCREEN } from '../models/ad22-screen.model';
import { adminQueryState, loadedRows } from '../../admin-screen-state';
import { renderDiscussionRow } from '../../admin-screen-renderers';

interface AD22Query {
  reason?: string;
  severity?: string;
  page: number;
}

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad22-page',
  templateUrl: './ad22-page.html',
})
export class AD22Page {
  readonly definition = AD22_SCREEN;
  private readonly api = inject(AD22ApiService);
  readonly filterReason = signal('');
  readonly filterSeverity = signal('');
  readonly query = signal<AD22Query>({ page: 1 });
  readonly viewState = adminQueryState(
    this.query,
    (query) => this.api.getReportedDiscussions(query),
    (page) => loadedRows(page.items.map(renderDiscussionRow), {
      page: page.pagination.page,
      total: page.pagination.total,
      totalPages: page.pagination.total_pages,
    }),
  );

  applyFilters(filters: Readonly<Record<string, string>>): void {
    this.query.set({
      reason: filters['reason'] || undefined,
      severity: filters['severity'] || undefined,
      page: 1,
    });
  }

  setFilterReason(value: string): void {
    this.filterReason.set(value);
  }

  setFilterSeverity(value: string): void {
    this.filterSeverity.set(value);
  }

  submitFilters(event: Event): void {
    event.preventDefault();
    this.applyFilters({ reason: this.filterReason(), severity: this.filterSeverity() });
  }

  clearFilters(): void {
    this.filterReason.set('');
    this.filterSeverity.set('');
    this.query.set({ page: 1 });
  }

  changePage(page: number): void {
    const pagination = this.viewState().pagination;
    if (pagination && Number.isSafeInteger(page) && page >= 1 && page <= pagination.totalPages) {
      this.query.update((query) => ({ ...query, page }));
    }
  }
}
