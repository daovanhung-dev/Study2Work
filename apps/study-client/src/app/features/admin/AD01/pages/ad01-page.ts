import { Component } from '@angular/core';

import { AD01Metrics } from '../ui/ad01-metrics';
import { AD01Overview } from '../ui/ad01-overview';
import { AD01Shortcuts } from '../ui/ad01-shortcuts';
import { AD01Icon } from '../ui/ad01-icon';
import { AD01_SCREEN_MODEL } from '../models/ad01-screen.model';

@Component({
  imports: [AD01Icon, AD01Metrics, AD01Overview, AD01Shortcuts],
  selector: 'study-ad01-page',
  styleUrl: './ad01-page.css',
  templateUrl: './ad01-page.html',
})
export class AD01Page {
  readonly screenModel = AD01_SCREEN_MODEL;
  readonly periods = ['Hôm nay', '7 ngày qua', '30 ngày qua'] as const;
}
