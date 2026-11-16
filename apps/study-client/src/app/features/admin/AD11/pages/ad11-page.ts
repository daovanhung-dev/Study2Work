import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { AD11ApiService } from '../data-access/ad11-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD11_SCREEN } from '../models/ad11-screen.model';
import { adminRouteState, loadedFields } from '../../admin-screen-state';
import { renderContentFields } from '../../admin-screen-renderers';
import type { AdminScreenField } from '../../../../shared/ui/admin-screen.model';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad11-page',
  templateUrl: './ad11-page.html',
})
export class AD11Page {
  readonly definition = AD11_SCREEN;
  private readonly api = inject(AD11ApiService);
  readonly viewState = adminRouteState(
    inject(ActivatedRoute),
    'contentId',
    (contentId) => this.api.getContent(contentId),
    (content) => loadedFields(renderContentFields(content)),
  );

  get metadataFields(): readonly AdminScreenField[] {
    return (this.viewState().fields ?? []).filter((field) => field.label !== 'Payload');
  }

  get payloadPreview(): string | null {
    return this.viewState().fields?.find((field) => field.label === 'Payload')?.value ?? null;
  }

  get contentTitle(): string {
    return this.viewState().fields?.find((field) => field.label === 'Tiêu đề')?.value ?? 'Nội dung thẩm định';
  }
}
