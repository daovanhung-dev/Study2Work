import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { AD12ApiService } from '../data-access/ad12-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD12_SCREEN } from '../models/ad12-screen.model';
import { adminQueryState, loadedRows } from '../../admin-screen-state';
import { isAdminLessonList } from '../../admin-api-guards';
import { renderLessonRow } from '../../admin-screen-renderers';

interface AD12Query {
  course?: string;
}

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad12-page',
  templateUrl: './ad12-page.html',
})
export class AD12Page {
  readonly definition = AD12_SCREEN;
  private readonly api = inject(AD12ApiService);
  readonly filterCourse = signal('');
  readonly query = signal<AD12Query>({});
  readonly viewState = adminQueryState(
    this.query,
    (query) => this.api.getLessons(query),
    (lessons) => isAdminLessonList(lessons)
      ? loadedRows(lessons.map(renderLessonRow))
      : { status: 'error', message: 'API #82 trả về danh sách bài học không hợp lệ.' },
    'DESIGN_RESOURCE_RETRIEVED',
  );

  get lessonCount(): string {
    return this.viewState().status === 'loaded'
      ? String(this.viewState().rows?.length ?? 0)
      : '—';
  }

  get isEmpty(): boolean {
    return this.viewState().status === 'loaded' && (this.viewState().rows?.length ?? 0) === 0;
  }

  setFilterCourse(value: string): void {
    this.filterCourse.set(value);
  }

  applyFilters(event: Event): void {
    event.preventDefault();
    const course = this.filterCourse();
    this.query.set(course === '' ? {} : { course });
  }

  clearFilters(): void {
    this.filterCourse.set('');
    this.query.set({});
  }

  refreshLessons(): void {
    this.query.update((query) => ({ ...query }));
  }
}
