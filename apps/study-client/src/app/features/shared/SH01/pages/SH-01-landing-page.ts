import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DestroyRef } from '@angular/core';
import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';

import { LandingApi } from '../data-access/SH-01-landing.service';
import type { Category, Course, LoadState } from '../models/SH-01-landing.models';
import { LandingView } from '../ui/SH-01-landing-view';

@Component({
  selector: 'study-landing-page',
  imports: [LandingView],
  templateUrl: './SH-01-landing.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class GuestLandingPage implements OnInit {
  private readonly destroyRef = inject(DestroyRef);
  private readonly api = inject(LandingApi);

  readonly categories = signal<Category[]>([]);
  readonly courses = signal<Course[]>([]);
  readonly categoryState = signal<LoadState>('loading');
  readonly courseState = signal<LoadState>('loading');

  ngOnInit(): void {
    this.loadCategories();
    this.loadCourses();
  }

  loadCategories(): void {
    this.categoryState.set('loading');
    this.api
      .getCategories()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (items) => {
          this.categories.set(items);
          this.categoryState.set(items.length ? 'ready' : 'empty');
        },
        error: () => this.categoryState.set('error'),
      });
  }

  loadCourses(): void {
    this.courseState.set('loading');
    this.api
      .getCourses()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (items) => {
          this.courses.set(items);
          this.courseState.set(items.length ? 'ready' : 'empty');
        },
        error: () => this.courseState.set('error'),
      });
  }
}
