import { Component } from '@angular/core';

import { AD01Header } from '../ui/ad01-header';
import { AD01Metrics } from '../ui/ad01-metrics';
import { AD01Overview } from '../ui/ad01-overview';
import { AD01Shortcuts } from '../ui/ad01-shortcuts';
import { AD01Icon } from '../ui/ad01-icon';

@Component({
  imports: [AD01Icon, AD01Header, AD01Metrics, AD01Overview, AD01Shortcuts],
  selector: 'study-ad01-page',
  styleUrl: './ad01-page.css',
  templateUrl: './ad01-page.html',
})
export class AD01Page {
  readonly periods = ['Hôm nay', '7 ngày qua', '30 ngày qua'] as const;
}
