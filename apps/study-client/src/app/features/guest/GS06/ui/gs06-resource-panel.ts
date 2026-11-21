import { Component, EventEmitter, Input, Output } from '@angular/core';
import { RouterLink } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import type { GS06ResourceScreenState } from '../models/gs06-resource-screen-state.model';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-gs06-resource-panel',
  styleUrl: './gs06-resource-panel.css',
  templateUrl: './gs06-resource-panel.html',
})
export class GS06ResourcePanel {
  @Input({ required: true }) courseId = '';
  @Input({ required: true }) state!: GS06ResourceScreenState;
  @Output() readonly retry = new EventEmitter<void>();
}
