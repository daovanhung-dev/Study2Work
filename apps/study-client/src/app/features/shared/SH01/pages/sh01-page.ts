import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { SH01CourseCard } from '../ui/sh01-course-card';
import { SH01CatalogService } from '../data-access/sh01-catalog.service';
import {
  readSH01Categories,
  readSH01PublishedCourses,
  type SH01Category,
  type SH01CategoryPage,
  type SH01PublicCourse,
  type SH01PublicCoursePage,
} from '../models/sh01-catalog.models';

type RegionState<T> =
  | { status: 'loading' }
  | { status: 'ready'; items: T[] }
  | { status: 'empty' }
  | { status: 'error' };

@Component({
  imports: [FormsModule, RouterLink, SH01CourseCard],
  selector: 'study-sh01-page',
  styleUrl: './sh01-page.css',
  templateUrl: './sh01-page.html',
})
export class SH01Page {
  private readonly destroyRef = inject(DestroyRef);
  private readonly catalogService = inject(SH01CatalogService);
  private readonly router = inject(Router);

  readonly searchQuery = signal('');
  readonly categoryState = signal<RegionState<SH01Category>>({ status: 'loading' });
  readonly courseState = signal<RegionState<SH01PublicCourse>>({ status: 'loading' });

  constructor() {
    this.loadCategories();
    this.loadCourses();
  }

  submitSearch(): void {
    const q = this.searchQuery().trim();
    if (!q) return;

    void this.router.navigate(['/courses/search'], { queryParams: { q } });
  }

  retryCategories(): void {
    this.loadCategories();
  }

  retryCourses(): void {
    this.loadCourses();
  }

  private loadCategories(): void {
    this.categoryState.set({ status: 'loading' });
    this.catalogService
      .getCategories()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response: ApiEnvelope<SH01CategoryPage>) => {
          const items = readSH01Categories(response);
          this.categoryState.set(
            items === null
              ? { status: 'error' }
              : items.length === 0
                ? { status: 'empty' }
                : { status: 'ready', items },
          );
        },
        error: () => this.categoryState.set({ status: 'error' }),
      });
  }

  private loadCourses(): void {
    this.courseState.set({ status: 'loading' });
    this.catalogService
      .getPublishedCourses()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response: ApiEnvelope<SH01PublicCoursePage>) => {
          const items = readSH01PublishedCourses(response);
          this.courseState.set(
            items === null
              ? { status: 'error' }
              : items.length === 0
                ? { status: 'empty' }
                : { status: 'ready', items },
          );
        },
        error: () => this.courseState.set({ status: 'error' }),
      });
  }
}
