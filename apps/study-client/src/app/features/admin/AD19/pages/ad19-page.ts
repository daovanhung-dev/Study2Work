import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { AD19ApiService } from '../data-access/ad19-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD19_SCREEN } from '../models/ad19-screen.model';
import { adminQueryState, loadedRows } from '../../admin-screen-state';
import { hasAD19NotificationsPageCountMismatch } from '../models/ad19-notifications.models';
import { renderNotificationRow } from '../../admin-screen-renderers';

interface AD19Query {
  status?: string;
  channel?: string;
  page: number;
}

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad19-page',
  templateUrl: './ad19-page.html',
})
export class AD19Page {
  readonly definition = AD19_SCREEN;
  private readonly api = inject(AD19ApiService);
  readonly filterStatus = signal('');
  readonly filterChannel = signal('');
  readonly query = signal<AD19Query>({ page: 1 });
  readonly snapshotMismatch = signal(false);
  readonly pageOutOfRange = signal(false);
  readonly viewState = adminQueryState(
    this.query,
    (query) => this.api.getNotifications(query),
    (page) => {
      const isOutOfRange = page.items.length === 0
        && page.pagination.page > Math.max(page.pagination.total_pages, 1);
      this.pageOutOfRange.set(isOutOfRange);
      this.snapshotMismatch.set(!isOutOfRange && hasAD19NotificationsPageCountMismatch(page));
      return loadedRows(page.items.map(renderNotificationRow), {
        page: page.pagination.page,
        total: page.pagination.total,
        totalPages: page.pagination.total_pages,
        size: page.pagination.size,
      });
    },
    'DESIGN_RESOURCE_RETRIEVED',
  );

  setFilterStatus(value: string): void {
    this.filterStatus.set(value);
  }

  setFilterChannel(value: string): void {
    this.filterChannel.set(value);
  }

  applyFilters(filters: Readonly<Record<string, string>>): void {
    this.clearPageFlags();
    this.query.set({
      status: filters['status'] || undefined,
      channel: filters['channel'] || undefined,
      page: 1,
    });
  }

  submitFilters(event: Event): void {
    event.preventDefault();
    this.applyFilters({ status: this.filterStatus(), channel: this.filterChannel() });
  }

  clearFilters(): void {
    this.clearPageFlags();
    this.filterStatus.set('');
    this.filterChannel.set('');
    this.query.set({ page: 1 });
  }

  refreshNotifications(): void {
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
