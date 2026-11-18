import type { SystemOperationsState } from '../models/SH-07-operations.models';
import { ChangeDetectionStrategy, Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'study-system-operations-view',
  imports: [CommonModule],
  templateUrl: './SH-07-operations-view.html',
  styleUrls: ['./SH-07-refined.css', './SH-07-tune.css'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SystemOperationsView {
  @Input({ required: true }) state!: SystemOperationsState;
  @Output() refresh = new EventEmitter<void>();
  mobileNavOpen = false;
}
