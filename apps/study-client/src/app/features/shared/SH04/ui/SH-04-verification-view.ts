import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

import type { VerificationState } from '../models/SH-04-verification.models';

@Component({
  selector: 'study-verification-view',
  templateUrl: './SH-04-verification-view.html',
  styleUrl: './SH-04-verification-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class VerificationView {
  @Input() state: VerificationState = 'missing';
  @Input() httpStatus: number | null = null;
}
