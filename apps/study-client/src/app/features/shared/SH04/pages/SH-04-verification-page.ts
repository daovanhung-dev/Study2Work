import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DestroyRef } from '@angular/core';

import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';

import { VerificationHandoffStore } from '../../verification-handoff';
import { VerificationApi } from '../data-access/SH-04-verification.service';
import type { VerificationState } from '../models/SH-04-verification.models';
import { VerificationView } from '../ui/SH-04-verification-view';

@Component({
  selector: 'study-verification-page',
  imports: [VerificationView],
  templateUrl: './SH-04-verification-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class VerificationPage implements OnInit {
  private readonly destroyRef = inject(DestroyRef);
  private readonly handoff = inject(VerificationHandoffStore);
  private readonly api = inject(VerificationApi);
  private dispatched = false;

  readonly state = signal<VerificationState>('missing');
  readonly httpStatus = signal<number | null>(null);

  ngOnInit(): void {
    const data = this.handoff.take();
    if (
      !data ||
      !Number.isSafeInteger(data.userId) ||
      data.userId <= 0 ||
      typeof data.email !== 'string' ||
      !data.email.trim()
    ) {
      this.state.set('missing');
      return;
    }

    if (this.dispatched) return;
    this.dispatched = true;
    this.state.set('pending');
    this.api
      .dispatch({ user_id: data.userId, email: data.email })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (result) => {
          this.httpStatus.set(result.httpStatus);
          this.state.set(result.state);
        },
      });
  }
}
