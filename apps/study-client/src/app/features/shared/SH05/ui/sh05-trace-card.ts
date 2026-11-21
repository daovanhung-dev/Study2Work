import { Component, Input, signal } from '@angular/core';

@Component({
  selector: 'study-sh05-trace-card',
  styleUrl: './sh05-trace-card.css',
  templateUrl: './sh05-trace-card.html',
})
export class SH05TraceCard {
  @Input({ required: true }) traceId = '';

  readonly copyFeedback = signal<'success' | 'failure' | null>(null);

  async copyTraceId(): Promise<void> {
    this.copyFeedback.set(null);

    try {
      const clipboard = globalThis.navigator?.clipboard;
      if (!clipboard || typeof clipboard.writeText !== 'function') {
        this.copyFeedback.set('failure');
        return;
      }

      await clipboard.writeText(this.traceId);
      this.copyFeedback.set('success');
    } catch {
      this.copyFeedback.set('failure');
    }
  }
}
