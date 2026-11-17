import { Component, Input, inject, signal } from '@angular/core';

import { SH05ErrorContextService } from '../data-access/sh05-error-context.service';
import type { SH05ErrorState } from '../models/sh05-error-state';
import { SH05TraceCard } from '../ui/sh05-trace-card';

@Component({
  imports: [SH05TraceCard],
  selector: 'study-sh05-page',
  styleUrl: './sh05-page.css',
  templateUrl: './sh05-page.html',
})
export class SH05Page {
  private readonly errorContext = inject(SH05ErrorContextService);

  readonly state = signal<SH05ErrorState | null>(null);

  @Input({ required: true })
  set errorResponse(value: unknown) {
    this.state.set(this.errorContext.normalize(value));
  }
}
