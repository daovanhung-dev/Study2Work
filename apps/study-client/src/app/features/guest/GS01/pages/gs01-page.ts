import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { catchError, concatMap, of, tap, type Subscription } from 'rxjs';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import type {
  GuestCategory,
  GuestCategoryPage,
  GuestPublicCoursePage,
} from '../../shared/models/guest-course.models';
import {
  isGuestCategoryPage,
  hasGuestPublicCoursePageCountMismatch,
  isGuestPublicCoursePage,
  isGuestResourceSuccessEnvelope,
} from '../../shared/models/guest-course.models';
import { GuestSiteLayout } from '../../shared/ui/guest-site-layout';
import { GS01CatalogService } from '../data-access/gs01-catalog.service';
import { GS01_SORT_OPTIONS, type GS01Sort } from '../models/gs01-catalog.models';
import { GS01Hero } from '../ui/gs01-hero';
import { GS01CourseCard } from '../ui/gs01-course-card';

type CategoryState =
  { status: 'loading' } | { status: 'ready'; items: GuestCategory[] } | { status: 'error' };

type CatalogState =
  | { status: 'loading' }
  | { status: 'ready'; result: GuestPublicCoursePage }
  | { status: 'empty' }
  | { status: 'out-of-range'; page: number; total: number; totalPages: number }
  | { status: 'error' };

@Component({
  imports: [GuestSiteLayout, GS01Hero, GS01CourseCard, RouterLink, StudyIcon],
  selector: 'study-gs01-page',
  styleUrl: './gs01-page.css',
  templateUrl: './gs01-page.html',
})
export class GS01Page {
  private readonly destroyRef = inject(DestroyRef);
  private readonly catalogService = inject(GS01CatalogService);

  readonly categoryState = signal<CategoryState>({ status: 'loading' });
  readonly catalogState = signal<CatalogState>({ status: 'loading' });
  readonly catalogSnapshotMismatch = signal(false);
  readonly sortOptions = GS01_SORT_OPTIONS;
  readonly selectedSort = signal<GS01Sort>('');
  private courseRequestSequence = 0;
  private activeCatalogRequest: Subscription | null = null;

  constructor() {
    this.loadInitialCatalog();
  }

  onSortChange(event: Event): void {
    const value = (event.currentTarget as HTMLSelectElement).value;
    const option = this.sortOptions.find((candidate) => candidate.value === value);
    if (!option) return;

    this.selectedSort.set(option.value);
    this.loadCourses(1, option.value);
  }

  goToPage(page: number): void {
    const state = this.catalogState();
    if (state.status !== 'ready' || this.catalogSnapshotMismatch()) return;

    const { page: currentPage, total_pages: totalPages } = state.result.pagination;
    if (!Number.isInteger(page) || page < 1 || page > totalPages || page === currentPage) return;

    this.loadCourses(page, this.selectedSort());
  }

  retryCatalog(): void {
    const state = this.catalogState();
    const page = state.status === 'ready' && this.catalogSnapshotMismatch()
      ? state.result.pagination.page
      : 1;
    this.loadCourses(page, this.selectedSort());
  }

  retryAll(): void {
    this.loadInitialCatalog();
  }

  private loadInitialCatalog(): void {
    this.cancelActiveCatalogRequest();
    const requestSequence = ++this.courseRequestSequence;
    this.categoryState.set({ status: 'loading' });
    this.catalogState.set({ status: 'loading' });
    this.catalogSnapshotMismatch.set(false);

    this.activeCatalogRequest = this.catalogService
      .getCategories()
      .pipe(
        catchError(() => {
          this.categoryState.set({ status: 'error' });
          return of(null);
        }),
        tap((response) => {
          if (response) this.applyCategoryResponse(response);
        }),
        concatMap(() => this.catalogService.getCourses({ page: 1, sort: this.selectedSort() })),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe({
        next: (response) => {
          if (requestSequence !== this.courseRequestSequence) return;
          this.applyCourseResponse(response, 1);
        },
        error: () => {
          if (requestSequence === this.courseRequestSequence) {
            this.catalogState.set({ status: 'error' });
          }
        },
      });
  }

  private loadCourses(page: number, sort: GS01Sort): void {
    this.cancelActiveCatalogRequest();
    const requestSequence = ++this.courseRequestSequence;
    this.catalogState.set({ status: 'loading' });
    this.catalogSnapshotMismatch.set(false);

    this.activeCatalogRequest = this.catalogService
      .getCourses({ page, sort })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          if (requestSequence !== this.courseRequestSequence) return;
          this.applyCourseResponse(response, page);
        },
        error: () => {
          if (requestSequence === this.courseRequestSequence) {
            this.catalogState.set({ status: 'error' });
          }
        },
      });
  }

  private applyCategoryResponse(response: ApiEnvelope<GuestCategoryPage>): void {
    const candidate: unknown = response;
    if (
      !isGuestResourceSuccessEnvelope(candidate) ||
      candidate.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isGuestCategoryPage(candidate.data)
    ) {
      this.categoryState.set({ status: 'error' });
      return;
    }

    this.categoryState.set({ status: 'ready', items: candidate.data.items });
  }

  private applyCourseResponse(
    response: ApiEnvelope<GuestPublicCoursePage>,
    requestedPage: number,
  ): void {
    const candidate: unknown = response;
    if (
      !isGuestResourceSuccessEnvelope(candidate) ||
      candidate.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isGuestPublicCoursePage(candidate.data)
    ) {
      this.catalogState.set({ status: 'error' });
      return;
    }

    const result = candidate.data;
    if (
      result.pagination.page !== requestedPage ||
      result.pagination.size !== 20 ||
      result.items.some((course) => course.status !== 'PUBLISHED')
    ) {
      this.catalogState.set({ status: 'error' });
      return;
    }

    if (
      result.items.length === 0 &&
      result.pagination.total > 0 &&
      requestedPage > result.pagination.total_pages
    ) {
      this.catalogState.set({
        status: 'out-of-range',
        page: requestedPage,
        total: result.pagination.total,
        totalPages: result.pagination.total_pages,
      });
    } else if (hasGuestPublicCoursePageCountMismatch(result)) {
      this.catalogSnapshotMismatch.set(true);
      this.catalogState.set({ status: 'ready', result });
    } else if (result.items.length > 0) {
      this.catalogState.set({ status: 'ready', result });
    } else if (result.pagination.total === 0) {
      this.catalogState.set({ status: 'empty' });
    } else {
      this.catalogState.set({ status: 'error' });
    }
  }

  private cancelActiveCatalogRequest(): void {
    this.activeCatalogRequest?.unsubscribe();
    this.activeCatalogRequest = null;
  }
}
