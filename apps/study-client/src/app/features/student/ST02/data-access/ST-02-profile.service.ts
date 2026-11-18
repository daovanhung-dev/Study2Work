import { HttpErrorResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { catchError, Observable, shareReplay, switchMap, throwError } from 'rxjs';
import { AuthSessionService } from '../../../../core/auth/auth-session.service';
import { StudentAccountProfileService } from '../../data-access/student-profile.service';
import type { StudentProfileDto } from '../models/ST-02-profile.models';

@Injectable({ providedIn: 'root' })
export class StudentProfileService {
  private readonly profile = inject(StudentAccountProfileService);
  private readonly session = inject(AuthSessionService);
  private cachedToken: string | null = null;
  private cachedProfile$: Observable<StudentProfileDto> | null = null;

  getProfile(): Observable<StudentProfileDto> {
    return this.session.ensureAccessToken().pipe(
      switchMap((token) => {
        if (!token) {
          this.invalidate();
          return throwError(() => new HttpErrorResponse({ status: 401 }));
        }
        if (this.cachedToken !== token || !this.cachedProfile$) {
          this.cachedToken = token;
          this.cachedProfile$ = this.profile.getProfile().pipe(
            catchError((error: unknown) => {
              if (this.cachedToken === token) this.invalidate();
              return throwError(() => error);
            }),
            shareReplay({ bufferSize: 1, refCount: false }),
          );
        }
        return this.cachedProfile$;
      }),
    );
  }

  invalidate(): void {
    this.cachedToken = null;
    this.cachedProfile$ = null;
  }
}
