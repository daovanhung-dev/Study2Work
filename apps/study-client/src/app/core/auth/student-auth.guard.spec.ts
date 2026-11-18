import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { firstValueFrom, of, type Observable } from 'rxjs';
import { describe, expect, it } from 'vitest';

import { AuthSessionService } from './auth-session.service';
import { studentAuthGuard } from './student-auth.guard';

describe('Student route guard', () => {
  it('sends guests to login and preserves the requested student route', async () => {
    TestBed.configureTestingModule({
      providers: [
        provideRouter([]),
        { provide: AuthSessionService, useValue: { ensureAccessToken: () => of(null), role: () => null } },
      ],
    });
    const result = await firstValueFrom(TestBed.runInInjectionContext(() =>
      studentAuthGuard({} as never, { url: '/student/courses' } as never) as unknown as Observable<unknown>,
    ));
    expect(TestBed.inject(Router).serializeUrl(result as never)).toBe('/login?returnUrl=%2Fstudent%2Fcourses');
  });

  it('allows an authenticated student', async () => {
    TestBed.configureTestingModule({
      providers: [
        provideRouter([]),
        { provide: AuthSessionService, useValue: { ensureAccessToken: () => of('access'), role: () => 'STUDENT' } },
      ],
    });
    const result = await firstValueFrom(TestBed.runInInjectionContext(() =>
      studentAuthGuard({} as never, { url: '/student' } as never) as unknown as Observable<unknown>,
    ));
    expect(result).toBe(true);
  });
});
