import { Injectable } from '@angular/core';

/** Availability of the screen's DD-backed data source. No synthetic API result. */
@Injectable({ providedIn: 'root' })
export class SystemOperationsService {
  /** DD gate: no verified data contract is available for this screen. */
  readonly status = 'blocked' as const;
}
