import { Component } from '@angular/core';

import type { GS06ResourceScreenState } from '../models/gs06-resource-screen-state.model';
import { GS06UnavailablePanel } from '../ui/gs06-unavailable-panel';

@Component({
  imports: [GS06UnavailablePanel],
  selector: 'study-gs06-page',
  styleUrl: './gs06-page.css',
  templateUrl: './gs06-page.html',
})
export class GS06Page {
  readonly state: GS06ResourceScreenState = 'contract-blocked';
}
