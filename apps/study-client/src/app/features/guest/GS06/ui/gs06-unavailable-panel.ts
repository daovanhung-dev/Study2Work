import { Component, Input } from '@angular/core';

import type { GS06ResourceScreenState } from '../models/gs06-resource-screen-state.model';
import { StudyIcon } from '../../../../shared/ui/study-icon';

@Component({
  imports: [StudyIcon],
  selector: 'study-gs06-unavailable-panel',
  styleUrl: './gs06-unavailable-panel.css',
  templateUrl: './gs06-unavailable-panel.html',
})
export class GS06UnavailablePanel {
  @Input({ required: true }) state!: GS06ResourceScreenState;
}
