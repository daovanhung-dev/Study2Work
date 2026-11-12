import { Component, Input } from '@angular/core';

import type { ContentKpiSummaryVm } from '../models/me06-content.models';

@Component({
  selector: 'study-me06-kpi-strip',
  styleUrl: './me06-kpi-strip.css',
  templateUrl: './me06-kpi-strip.html',
})
export class Me06KpiStrip {
  @Input({ required: true }) summary!: ContentKpiSummaryVm;
  @Input() dataLoaded = false;
}
