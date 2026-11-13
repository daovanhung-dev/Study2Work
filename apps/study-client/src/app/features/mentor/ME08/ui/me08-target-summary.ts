import { Component, Input } from '@angular/core';

import type { Me08TargetInspectionVm } from '../models/me08-actions.models';

@Component({
  selector: 'study-me08-target-summary',
  styleUrl: './me08-target-summary.css',
  templateUrl: './me08-target-summary.html',
})
export class Me08TargetSummary {
  @Input() inspection: Me08TargetInspectionVm | null = null;
  @Input() contentId: number | null = null;
  @Input() courseId: number | null = null;
}
