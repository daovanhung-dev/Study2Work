import { Component, EventEmitter, Input, Output } from '@angular/core';

import { type SupportRequestDetailDto } from '../models/me12-thread.models';

@Component({
  selector: 'study-me12-thread-panel',
  styleUrl: './me12-thread-panel.css',
  templateUrl: './me12-thread-panel.html',
})
export class Me12ThreadPanel {
  @Input() requestDetail: SupportRequestDetailDto | null = null;
  @Input() refreshing = false;

  @Output() readonly refreshThread = new EventEmitter<void>();
}
