import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { map } from 'rxjs';

import { AuthSessionService } from './auth-session.service';

export const studentAuthGuard: CanActivateFn = (_route, state) => {
  const session = inject(AuthSessionService);
  const router = inject(Router);
  return session.ensureAccessToken().pipe(
    map((token) => {
      if (!token) return router.createUrlTree(['/login'], { queryParams: { returnUrl: state.url } });
      return session.role() === 'STUDENT' ? true : router.createUrlTree(['/forbidden']);
    }),
  );
};
