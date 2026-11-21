import { Injectable } from '@angular/core';

import { normalizeAuthorizationError } from '../../../../core/auth/authorization-error';
import type { SH05ErrorState } from '../models/sh05-error-state';

@Injectable({ providedIn: 'root' })
export class SH05ErrorContextService {
  normalize(error: unknown): SH05ErrorState | null {
    return normalizeAuthorizationError(error);
  }
}
