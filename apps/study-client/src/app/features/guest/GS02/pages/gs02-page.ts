import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, Router } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import { GS02SearchService } from '../data-access/gs02-search.service';
import { normalizeGS02Query, type GS02SearchState } from '../models/gs02-search.models';
import { GS02CourseCard } from '../ui/gs02-course-card';

@Component({
  imports: [GS02CourseCard, StudyIcon],
  selector: 'study-gs02-page',
  styleUrl: './gs02-page.css',
  templateUrl: './gs02-page.html',
})
export class GS02Page {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);
  private readonly searchService = inject(GS02SearchService);

  readonly queryInput = signal('');
  readonly state = signal<GS02SearchState>({ status: 'prompt' });

  private activeQuery: string | null = null;
  private requestSequence = 0;

  constructor() {
    this.route.queryParamMap.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((params) => {
      const rawQuery = params.get('q') ?? '';
      const query = normalizeGS02Query(rawQuery);
      this.queryInput.set(rawQuery);

      if (query === this.activeQuery) return;

      this.activeQuery = query;
      if (!query) {
        this.requestSequence += 1;
        this.state.set({ status: 'prompt' });
        return;
      }

      this.search(query, 1);
    });
  }

  onQueryInput(event: Event): void {
    this.queryInput.set((event.currentTarget as HTMLInputElement).value);
  }

  submitSearch(event: Event): void {
    event.preventDefault();
    const query = normalizeGS02Query(this.queryInput());
    this.queryInput.set(query);

    if (!query) {
      this.activeQuery = '';
      this.requestSequence += 1;
      this.state.set({ status: 'prompt' });
      void this.router.navigate([], {
        relativeTo: this.route,
        queryParams: { q: null },
      });
      return;
    }

    this.activeQuery = query;
    this.search(query, 1);
    void this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { q: query },
    });
  }

  goToPage(page: number): void {
    const currentState = this.state();
    if (currentState.status !== 'ready') return;

    const { page: currentPage, total_pages: totalPages } = currentState.result.pagination;
    if (!Number.isInteger(page) || page < 1 || page > totalPages || page === currentPage) return;

    this.search(currentState.query, page);
  }

  private search(query: string, page: number): void {
    const requestSequence = ++this.requestSequence;
    this.state.set({ status: 'loading', query, page });

    this.searchService
      .search(query, page)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          if (requestSequence !== this.requestSequence) return;
          if (!response.success || response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
            this.state.set({ status: 'error', query, page });
            return;
          }

          const result = response.data;
          if (result.items.length > 0) {
            this.state.set({ status: 'ready', query, result });
          } else if (result.pagination.total === 0) {
            this.state.set({ status: 'no-results', query });
          } else if (page > result.pagination.total_pages) {
            this.state.set({
              status: 'out-of-range',
              query,
              page,
              total: result.pagination.total,
              totalPages: result.pagination.total_pages,
            });
          } else {
            this.state.set({ status: 'error', query, page });
          }
        },
        error: () => {
          if (requestSequence !== this.requestSequence) return;
          this.state.set({ status: 'error', query, page });
        },
      });
  }
}
