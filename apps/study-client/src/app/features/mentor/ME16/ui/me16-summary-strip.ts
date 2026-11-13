import { Component, Input } from '@angular/core';

import { type Me16RosterKpiVm } from '../models/me16-progress.models';

@Component({
  selector: 'study-me16-summary-strip',
  styleUrl: './me16-summary-strip.css',
  templateUrl: './me16-summary-strip.html',
})
export class Me16SummaryStrip {
  @Input() kpi: Me16RosterKpiVm = {
    totalStudents: 0,
    completedAllCount: 0,
    inProgressCount: 0,
    notStartedCount: 0,
    averagePercent: 0,
  };
  @Input() dataLoaded = false;
}
