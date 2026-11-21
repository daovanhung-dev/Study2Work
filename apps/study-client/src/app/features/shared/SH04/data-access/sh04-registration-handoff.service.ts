import { Injectable } from '@angular/core';

import type { SH04RegistrationHandoff } from '../models/sh04-verification.models';

@Injectable({ providedIn: 'root' })
export class SH04RegistrationHandoffService {
  private pendingHandoff: SH04RegistrationHandoff | null = null;

  set(handoff: SH04RegistrationHandoff): boolean {
    if (
      !Number.isSafeInteger(handoff.userId) ||
      handoff.userId <= 0 ||
      typeof handoff.email !== 'string' ||
      !handoff.email.trim()
    ) {
      this.clear();
      return false;
    }

    this.pendingHandoff = { userId: handoff.userId, email: handoff.email };
    return true;
  }

  consume(): SH04RegistrationHandoff | null {
    const handoff = this.pendingHandoff;
    this.pendingHandoff = null;
    return handoff;
  }

  clear(): void {
    this.pendingHandoff = null;
  }
}
