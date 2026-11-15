import { Component, inject, signal } from '@angular/core';

import { AD12ApiService } from '../data-access/ad12-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD12_SCREEN } from '../models/ad12-screen.model';
import { adminQueryState, loadedRows } from '../../admin-screen-state';
import { renderLessonRow } from '../../admin-screen-renderers';

type AD12Query = Record<string, never>;

@Component({
  imports: [StudyIcon],
  selector: 'study-ad12-page',
  templateUrl: './ad12-page.html',
})
export class AD12Page {
  readonly definition = AD12_SCREEN;
  private readonly api = inject(AD12ApiService);
  readonly query = signal<AD12Query>({});
  readonly viewState = adminQueryState(
    this.query,
    (query) => this.api.getLessons(query),
    (lessons) => loadedRows(lessons.map(renderLessonRow)),
  );

  get lessonCount(): string {
    return this.viewState().status === 'loaded'
      ? String(this.viewState().rows?.length ?? 0)
      : '—';
  }

  get isEmpty(): boolean {
    return this.viewState().status === 'loaded' && (this.viewState().rows?.length ?? 0) === 0;
  }
}
