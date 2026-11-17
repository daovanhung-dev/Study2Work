import type { AccessFailureViewModel } from '../models/SH-05-forbidden.models';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'study-system-forbidden-view',
  imports: [CommonModule],
  templateUrl: './SH-05-forbidden-view.html',
  styleUrl: './SH-05-forbidden-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SystemForbiddenView {
  @Input({ required: true }) state!: AccessFailureViewModel;
}
