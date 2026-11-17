import { Component } from '@angular/core';

import { GuestSiteLayout } from '../../shared/ui/guest-site-layout';
import type { GS07ResourceScreenState } from '../models/gs07-resource-screen-state.model';
import { GS07UnavailableNotice } from '../ui/gs07-unavailable-notice';

@Component({
  imports: [GuestSiteLayout, GS07UnavailableNotice],
  selector: 'study-gs07-page',
  styleUrl: './gs07-page.css',
  templateUrl: './gs07-page.html',
})
export class GS07Page {
  readonly state: GS07ResourceScreenState = 'contract-blocked';
}
