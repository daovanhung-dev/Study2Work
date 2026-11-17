import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, inject, Input, signal } from '@angular/core';
import { catchError, map, of, Subject, switchMap, tap } from 'rxjs';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { GS05ReviewsService } from '../data-access/gs05-reviews.service';
import {
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
            map((response) => this.mapResponse(response)),
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

  private requestPage(page: number): void {
    this.pageRequests.next({ courseId: this.activeCourseId, page });
  }

  private mapResponse(response: ApiEnvelope<GS05CourseReviewsPage>): GS05ReviewsState {
    if (!response.success || response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
      return { status: 'error' };
    }

    const items = toGS05ReviewItems(response.data.items);
    if (items.length === 0) return { status: 'empty' };

    return {
      status: 'ready',
      items,
      page: response.data.pagination.page,
      totalPages: response.data.pagination.total_pages,
    };
  }

  private mapHttpError(error: unknown): GS05ReviewsState {
    return error instanceof HttpErrorResponse && error.status === 404
      ? { status: 'not-found' }
      : { status: 'error' };
  }
}
