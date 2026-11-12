import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { NotificationStatusSummaryVm } from '../models/me15-notification-status.models';

@Component({
  selector: 'app-me15-status-summary',
  imports: [],
  templateUrl: './me15-status-summary.html',
  styleUrl: './me15-status-summary.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Me15StatusSummaryComponent {
  readonly summary = input.required<NotificationStatusSummaryVm>();
}
