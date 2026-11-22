import { Component, Input } from '@angular/core';

import { AD01Icon } from './ad01-icon';
import type { AD01MetricCardModel } from '../models/ad01-report.model';

@Component({
  imports: [AD01Icon],
  selector: 'study-ad01-metrics',
  styleUrl: './ad01-metrics.css',
  templateUrl: './ad01-metrics.html',
})
export class AD01Metrics {
  @Input() metrics: readonly AD01MetricCardModel[] = [];
  @Input() state: 'loading' | 'ready' | 'error' = 'loading';
}
