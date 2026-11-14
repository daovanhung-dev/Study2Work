import type { NotFoundViewModel } from '../models/SH-06-not-found.models';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'study-system-not-found-view',
  imports: [CommonModule],
  templateUrl: './SH-06-not-found-view.html',
  styleUrl: './SH-06-not-found-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SystemNotFoundView {
  @Input({ required: true }) state!: NotFoundViewModel;
}
