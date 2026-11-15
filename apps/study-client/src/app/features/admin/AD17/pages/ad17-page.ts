import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { AD17ApiService } from '../data-access/ad17-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD17_SCREEN } from '../models/ad17-screen.model';
import { adminRouteState, loadedMetrics } from '../../admin-screen-state';
import { renderQuizStatistics } from '../../admin-screen-renderers';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad17-page',
  templateUrl: './ad17-page.html',
})
export class AD17Page {
  readonly definition = AD17_SCREEN;
  private readonly api = inject(AD17ApiService);
  readonly viewState = adminRouteState(
    inject(ActivatedRoute),
    'quizId',
    (quizId) => this.api.getStatistics(quizId),
    (statistics) => loadedMetrics(renderQuizStatistics(statistics)),
  );

  get quizId(): string {
    return this.viewState().metrics?.find((metric) => metric.label === 'Mã Quiz')?.value ?? '—';
  }

  get metricCards() {
    return this.viewState().metrics?.filter((metric) => metric.label !== 'Mã Quiz') ?? [];
  }
}
