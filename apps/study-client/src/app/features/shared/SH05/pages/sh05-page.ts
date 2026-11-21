import { Component, Input, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { SH05ErrorContextService } from '../data-access/sh05-error-context.service';
import type { SH05ErrorState } from '../models/sh05-error-state';
import { SH05TraceCard } from '../ui/sh05-trace-card';

@Component({
  imports: [RouterLink, SH05TraceCard],
  selector: 'study-sh05-page',
  styleUrl: './sh05-page.css',
  templateUrl: './sh05-page.html',
})
export class SH05Page implements OnInit {
  private readonly errorContext = inject(SH05ErrorContextService);

  readonly state = signal<SH05ErrorState | null>(null);
  readonly routeHandoff = signal(false);
  readonly errorInputReceived = signal(false);
  readonly returnTo = signal('/');

  ngOnInit(): void {
    const navigationState = typeof window === 'undefined' ? null : window.history.state;
    const candidate = navigationState?.['sh05Error'];
    const errorState = asSH05ErrorState(candidate);
    this.returnTo.set(safeInternalRoute(navigationState?.['sh05ReturnTo']));
    if (!errorState) return;

    this.state.set(errorState);
    this.routeHandoff.set(true);
  }

  @Input()
  set errorResponse(value: unknown) {
    this.errorInputReceived.set(true);
    this.state.set(this.errorContext.normalize(value));
    this.routeHandoff.set(false);
  }
}

function safeInternalRoute(value: unknown): string {
  if (
    typeof value !== 'string' ||
    !value.startsWith('/') ||
    value.startsWith('//') ||
    value.includes('\\') ||
    /[\u0000-\u001f]/.test(value)
  ) {
    return '/';
  }
  return value;
}

function asSH05ErrorState(value: unknown): SH05ErrorState | null {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return null;
  const candidate = value as Record<string, unknown>;
  const message = candidate['message'];
  const traceId = candidate['traceId'];
  const traceIdConflict = candidate['traceIdConflict'];

  if (
    typeof message !== 'string' ||
    message.trim().length === 0 ||
    (traceId !== null && typeof traceId !== 'string') ||
    typeof traceIdConflict !== 'boolean'
  ) {
    return null;
  }

  if (candidate['kind'] === 'authentication-required' && candidate['status'] === 401) {
    return {
      kind: 'authentication-required',
      status: 401,
      message,
      traceId: typeof traceId === 'string' && traceId.trim() ? traceId : null,
      traceIdConflict,
    };
  }

  if (candidate['kind'] === 'access-denied' && candidate['status'] === 403) {
    return {
      kind: 'access-denied',
      status: 403,
      message,
      traceId: typeof traceId === 'string' && traceId.trim() ? traceId : null,
      traceIdConflict,
    };
  }

  return null;
}
