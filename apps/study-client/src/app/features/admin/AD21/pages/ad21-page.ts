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
  );

  valueFor(label: string): string {
    return this.viewState().fields?.find((field) => field.label === label)?.value ?? '—';
  }
}
