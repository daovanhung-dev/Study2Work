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
    isPositiveSignedInt64QuizId,
    'Mã Quiz trên đường dẫn phải là số nguyên dương trong giới hạn signed 64-bit.',
  );

  get quizId(): string {
    return this.viewState().metrics?.find((metric) => metric.label === 'Mã Quiz')?.value ?? '—';
  }

  get metricCards() {
    return this.viewState().metrics?.filter((metric) => metric.label !== 'Mã Quiz') ?? [];
  }
}

function isPositiveSignedInt64QuizId(value: string): boolean {
  const match = /^[0-9]+$/.exec(value);
  if (value.length > 19 || match?.[0] !== value) {
    return false;
  }

  const digits = value.replace(/^0+/, '') || '0';
  const max = '9223372036854775807';
  return digits !== '0'
    && (digits.length < max.length || (digits.length === max.length && digits <= max));
}
