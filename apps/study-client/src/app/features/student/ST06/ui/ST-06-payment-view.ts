import type { StudentPaymentState } from '../models/ST-06-payment.models';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'study-student-payment-view',
  imports: [CommonModule],
  templateUrl: './ST-06-payment-view.html',
  styleUrl: './ST-06-payment-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentPaymentView {
  @Input({ required: true }) state!: StudentPaymentState;
}
