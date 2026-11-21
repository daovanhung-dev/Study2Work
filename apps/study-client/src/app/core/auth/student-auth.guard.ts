import { inject } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { CanActivateChildFn, Router } from '@angular/router';
import { catchError, map, of, switchMap } from 'rxjs';

import { StudentAccountProfileService } from '../../features/student/data-access/student-profile.service';
import { StudyAuthSessionService } from './study-auth-session.service';

export const studentAuthGuard: CanActivateChildFn = () => {
  const session = inject(StudyAuthSessionService);
  const profileApi = inject(StudentAccountProfileService);
  const router = inject(Router);

  if (session.isStudentProfileVerified()) return true;

  const token$ = session.accessToken()
    ? of(session.accessToken())
    : session.refreshAccessToken();

  return token$.pipe(
    switchMap((token) => (token ? profileApi.getProfile() : of(null))),
    map((profile) => {
      if (!profile || profile.role.toUpperCase() !== 'STUDENT') {
        session.clearAccessToken();
        return router.createUrlTree(['/login']);
      }
      session.markStudentProfileVerified();
      return true;
    }),
    catchError((error: unknown) => {
      session.clearAccessToken();
      if (error instanceof HttpErrorResponse && error.status === 403) {
        return session.logout().pipe(
          map(() => router.createUrlTree(['/forbidden'])),
          catchError(() => of(router.createUrlTree(['/forbidden']))),
        );
      }
      return of(router.createUrlTree(['/login']));
    }),
  );
};
