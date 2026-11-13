import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import {
  NotificationDeliveryState,
  NotificationStatusItemVm,
} from '../models/me15-notification-status.models';

@Component({
  selector: 'app-me15-status-table',
  imports: [],
  templateUrl: './me15-status-table.html',
  styleUrl: './me15-status-table.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Me15StatusTableComponent {
  readonly items = input.required<NotificationStatusItemVm[]>();

  getStatusLabel(status: NotificationDeliveryState): string {
    if (status === 'SENT') {
      return 'Đã gửi (SENT)';
    }
    if (status === 'FAILED') {
      return 'Thất bại (FAILED)';
    }
    return 'Đang xếp hàng (QUEUED)';
  }
}
