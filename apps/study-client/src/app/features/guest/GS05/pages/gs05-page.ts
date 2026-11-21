import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, inject, Input, signal } from '@angular/core';
import { catchError, map, of, Subject, switchMap, tap } from 'rxjs';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { isGuestResourceSuccessEnvelope } from '../../shared/models/guest-course.models';
import { GS05ReviewsService } from '../data-access/gs05-reviews.service';
import {
  isGS05CourseReviewsPage,
  toGS05ReviewItems,
  type GS05CourseReviewsPage,
  type GS05ReviewsState,
} from '../models/gs05-reviews.models';
import { GS05ReviewsPanel } from '../ui/gs05-reviews-panel';

interface ReviewsRequest {
  courseId: string;
  page: number;
}

@Component({
  imports: [GS05ReviewsPanel],
  selector: 'study-gs05-page',
  styleUrl: './gs05-page.css',
  templateUrl: './gs05-page.html',
})
export class GS05Page {
  private readonly destroyRef = inject(DestroyRef);
  private readonly reviewsService = inject(GS05ReviewsService);
  private readonly pageRequests = new Subject<ReviewsRequest>();
  private activeCourseId = '';
  private lastRequestedPage = 1;

  readonly state = signal<GS05ReviewsState>({ status: 'idle' });

  @Input({ required: true })
  set courseId(value: string) {
    if (!value || value === this.activeCourseId) return;
    this.activeCourseId = value;
    this.requestPage(1);
  }

  constructor() {
    this.pageRequests
      .pipe(
        tap(() => this.state.set({ status: 'loading' })),
        switchMap(({ courseId, page }) =>
          this.reviewsService.getCourseReviews(courseId, page).pipe(
            map((response) => this.mapResponse(response, page)),
            catchError((error: unknown) => of(this.mapHttpError(error))),
          ),
        ),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((state) => this.state.set(state));
  }

  selectPage(page: number): void {
    const state = this.state();
    if (
      state.status !== 'ready' ||
      !Number.isInteger(page) ||
      page < 1 ||
      page > state.totalPages ||
      page === state.page
    ) {
      return;
    }

    this.requestPage(page);
  }

  retryPage(): void {
    if (this.activeCourseId) this.requestPage(this.lastRequestedPage);
  }

  loadFirstPage(): void {
    if (this.activeCourseId) this.requestPage(1);
  }

  private requestPage(page: number): void {
    this.lastRequestedPage = page;
    this.pageRequests.next({ courseId: this.activeCourseId, page });
  }

  private mapResponse(
    response: ApiEnvelope<GS05CourseReviewsPage>,
    requestedPage: number,
  ): GS05ReviewsState {
    const candidate: unknown = response;
    if (
      !isGuestResourceSuccessEnvelope(candidate) ||
      candidate.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isGS05CourseReviewsPage(candidate.data)
    ) {
      return { status: 'error' };
    }

    const result = candidate.data;
    if (result.pagination.page !== requestedPage) return { status: 'error' };
    if (result.items.length === 0 && result.pagination.total === 0) return { status: 'empty' };

    if (result.items.length === 0 && requestedPage > result.pagination.total_pages) {
      return { status: 'out-of-range', page: requestedPage };
    }

    const expectedItems = Math.min(
      20,
      Math.max(result.pagination.total - (requestedPage - 1) * 20, 0),
    );
    const snapshotMismatch = result.items.length !== expectedItems;

    return {
      status: 'ready',
      items: toGS05ReviewItems(result.items),
      page: result.pagination.page,
      totalPages: result.pagination.total_pages,
      snapshotMismatch,
    };
  }

  private mapHttpError(error: unknown): GS05ReviewsState {
    return error instanceof HttpErrorResponse && error.status === 404
      ? { status: 'not-found' }
      : { status: 'error' };
  }
}
