import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { SH04RegistrationHandoffService } from '../data-access/sh04-registration-handoff.service';
import { SH04VerificationService } from '../data-access/sh04-verification.service';
import type {
  SH04RegistrationHandoff,
  SH04VerificationScreenState,
} from '../models/sh04-verification.models';

@Component({
  imports: [RouterLink],
  selector: 'study-sh04-page',
  styleUrl: './sh04-page.css',
  templateUrl: './sh04-page.html',
})
export class SH04Page {
  private readonly destroyRef = inject(DestroyRef);
  private readonly handoffs = inject(SH04RegistrationHandoffService);
  private readonly verification = inject(SH04VerificationService);
  private readonly registration: SH04RegistrationHandoff | null = this.handoffs.consume();

  readonly state = signal<SH04VerificationScreenState>(
    this.registration
      ? { status: 'ready', email: this.registration.email }
      : { status: 'missing-handoff' },
  );

  sendRequest(): void {
    const registration = this.registration;
    if (!registration || this.state().status !== 'ready') return;

    this.state.set({ status: 'submitting', email: registration.email });
    this.verification
      .sendRequest(registration.userId, registration.email)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          const envelope = response.body;
          if (
            response.status !== 202 ||
            !envelope ||
            !envelope.success ||
            envelope.businessCode !== 'DESIGN_OPERATION_ACCEPTED'
          ) {
            this.state.set({ status: 'outcome-unknown' });
            return;
          }

          const providerStatus = readProviderStatus(envelope.data);
          if (providerStatus === 'accepted') {
            this.state.set({ status: 'accepted', email: registration.email });
          } else if (providerStatus) {
            this.state.set({ status: 'provider-status-unknown', email: registration.email });
          } else {
            this.state.set({ status: 'outcome-unknown' });
          }
        },
        error: (error: unknown) => {
          if (error instanceof HttpErrorResponse && error.status === 422) {
            this.state.set({ status: 'invalid-request' });
            return;
          }
          if (error instanceof HttpErrorResponse && error.status === 0) {
            this.state.set({ status: 'outcome-unknown' });
            return;
          }
          this.state.set({ status: 'request-error' });
        },
      });
  }
}

function readProviderStatus(value: unknown): string | null {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return null;
  const status = (value as Record<string, unknown>)['status'];
  return typeof status === 'string' && status.trim() ? status : null;
}
