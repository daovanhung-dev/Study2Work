import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

import type { Category, Course, LoadState } from '../models/SH-01-landing.models';

@Component({
  selector: 'study-landing-view',
  imports: [CommonModule, FormsModule],
  templateUrl: './SH-01-landing-view.html',
  styleUrl: './SH-01-landing-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LandingView {
  @Input() categories: Category[] = [];
  @Input() courses: Course[] = [];
  @Input() categoryState: LoadState = 'loading';
  @Input() courseState: LoadState = 'loading';
  @Output() retryCategories = new EventEmitter<void>();
  @Output() retryCourses = new EventEmitter<void>();

  searchQuery = '';
  mobileNavOpen = false;
  readonly partners = ['VNG Corporation', 'FPT Software', 'Shopee', 'Techcombank', 'Viettel Group'];

  get filteredCourses(): Course[] {
    const query = this.searchQuery.trim().toLocaleLowerCase();
    return query
      ? this.courses.filter((course) => course.title.toLocaleLowerCase().includes(query))
      : this.courses;
  }

  trackCategory(_index: number, category: Category): number {
    return category.id;
  }

  trackCourse(_index: number, course: Course): number {
    return course.id;
  }

  onHeroSearch(event: Event): void {
    event.preventDefault();
    document.getElementById('featured-courses-section')?.scrollIntoView({ behavior: 'smooth' });
  }
}
