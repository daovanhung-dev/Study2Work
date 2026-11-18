import type { AccessFailureViewModel } from '../models/SH-05-forbidden.models';
import { ChangeDetectionStrategy, Component, Input, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'study-system-forbidden-view',
  imports: [CommonModule],
  templateUrl: './SH-05-forbidden-view.html',
  styleUrl: './SH-05-forbidden-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SystemForbiddenView {
  @Input({ required: true }) state!: AccessFailureViewModel;
  readonly copyFeedback = signal('');

  loginHref(): string {
    return this.state.returnUrl
      ? `/login?returnUrl=${encodeURIComponent(this.state.returnUrl)}`
      : '/login';
  }

  async copyTraceId(): Promise<void> {
    if (!this.state.traceId) return;
    try {
      await navigator.clipboard.writeText(this.state.traceId);
      this.copyFeedback.set('Đã sao chép Trace ID');
    } catch {
      this.copyFeedback.set('Không thể sao chép. Vui lòng chọn và sao chép mã thủ công.');
    }
  }
}
