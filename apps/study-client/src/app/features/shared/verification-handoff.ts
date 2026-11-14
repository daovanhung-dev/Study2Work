import { Injectable } from '@angular/core';

export interface VerificationHandoff {
  userId: number;
  email: string;
}

/** Bàn giao một lần giữa SH-03 và SH-04; không ghi vào URL hoặc browser storage. */
@Injectable({ providedIn: 'root' })
export class VerificationHandoffStore {
  private pending: VerificationHandoff | null = null;

  set(value: VerificationHandoff): void {
    this.pending = value;
  }

  take(): VerificationHandoff | null {
    const value = this.pending;
    this.pending = null;
    return value;
  }

  clear(): void {
    this.pending = null;
  }
}
