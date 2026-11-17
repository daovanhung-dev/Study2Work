import { Component, Input } from '@angular/core';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import type { GS07ResourceScreenState } from '../models/gs07-resource-screen-state.model';

@Component({
  imports: [StudyIcon],
  selector: 'study-gs07-unavailable-notice',
  styleUrl: './gs07-unavailable-notice.css',
  templateUrl: './gs07-unavailable-notice.html',
})
export class GS07UnavailableNotice {
  @Input({ required: true }) state!: GS07ResourceScreenState;
}
