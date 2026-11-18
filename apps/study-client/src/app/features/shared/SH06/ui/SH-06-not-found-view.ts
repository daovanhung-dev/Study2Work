import type { NotFoundViewModel } from '../models/SH-06-not-found.models';
import type { Course } from '../../SH01/models/SH-01-landing.models';
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
  @Input() courses: Course[] | null = null;
  mobileNavOpen = false;

  formatPrice(price: string): string {
    const amount = Number(price);
    return Number.isFinite(amount) && amount === 0
      ? 'Miễn phí'
      : `${new Intl.NumberFormat('vi-VN').format(amount)} ₫`;
  }
}
