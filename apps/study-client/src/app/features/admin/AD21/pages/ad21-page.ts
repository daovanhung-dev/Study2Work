import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { AD21ApiService } from '../data-access/ad21-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD21_SCREEN } from '../models/ad21-screen.model';
import { adminRouteState, loadedFields } from '../../admin-screen-state';
import { renderNotificationStatusFields } from '../../admin-screen-renderers';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad21-page',
  templateUrl: './ad21-page.html',
})
export class AD21Page {
  readonly definition = AD21_SCREEN;
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(AD21ApiService);
  readonly viewState = adminRouteState(
    this.route,
    'notificationId',
    (notificationId) => this.api.getStatus(notificationId),
    (notification) => loadedFields(renderNotificationStatusFields(notification)),
    isPositiveSignedInt64NotificationId,
    'Mã thông báo trên đường dẫn phải là số nguyên dương trong giới hạn signed 64-bit.',
  );

  valueFor(label: string): string {
    return this.viewState().fields?.find((field) => field.label === label)?.value ?? '—';
  }
}

function isPositiveSignedInt64NotificationId(value: string): boolean {
  const match = /^[0-9]+$/.exec(value);
  if (value.length > 19 || match?.[0] !== value) {
    return false;
  }

  const digits = value.replace(/^0+/, '') || '0';
  const max = '9223372036854775807';
  return digits !== '0'
    && (digits.length < max.length || (digits.length === max.length && digits <= max));
}
