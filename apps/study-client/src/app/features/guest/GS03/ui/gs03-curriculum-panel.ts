import { Component, Input } from '@angular/core';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import type { GuestCurriculumState } from '../models/gs03-curriculum.models';

@Component({
  imports: [StudyIcon],
  selector: 'study-gs03-curriculum-panel',
  styleUrl: './gs03-curriculum-panel.css',
  templateUrl: './gs03-curriculum-panel.html',
})
export class GS03CurriculumPanel {
  @Input({ required: true }) state!: GuestCurriculumState;
}
