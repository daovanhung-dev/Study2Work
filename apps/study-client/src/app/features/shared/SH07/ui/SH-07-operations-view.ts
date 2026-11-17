import type { SystemOperationsState } from '../models/SH-07-operations.models';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'study-system-operations-view',
  imports: [CommonModule],
  templateUrl: './SH-07-operations-view.html',
  styleUrl: './SH-07-operations-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SystemOperationsView {
  @Input({ required: true }) state!: SystemOperationsState;
}
