import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { AD23ApiService } from '../data-access/ad23-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD23_SCREEN } from '../models/ad23-screen.model';
import { adminRouteState, loadedFields } from '../../admin-screen-state';
import { renderDiscussionComments, renderDiscussionFields } from '../../admin-screen-renderers';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad23-page',
  templateUrl: './ad23-page.html',
})
export class AD23Page {
  readonly definition = AD23_SCREEN;
  private readonly api = inject(AD23ApiService);
  readonly viewState = adminRouteState(
    inject(ActivatedRoute),
    'discussionId',
    (discussionId) => this.api.getDiscussion(discussionId),
    (page) => page.items[0]
      ? loadedFields(renderDiscussionFields(page.items[0]), renderDiscussionComments(page.items[0]))
      : { status: 'error', message: 'API #98 không trả thảo luận cho mã đã yêu cầu.' },
  );

  valueFor(label: string): string {
    return this.viewState().fields?.find((field) => field.label === label)?.value ?? '—';
  }

  get comments(): readonly string[] {
    return this.viewState().sections?.[0]?.items ?? [];
  }
}
