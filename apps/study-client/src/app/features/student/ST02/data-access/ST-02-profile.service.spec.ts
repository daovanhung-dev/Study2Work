import { TestBed } from '@angular/core/testing';
import { firstValueFrom, of, throwError } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { AuthSessionService } from '../../../../core/auth/auth-session.service';
import { StudentAccountProfileService } from '../../data-access/student-profile.service';
import type { StudentProfileDto } from '../models/ST-02-profile.models';
import { StudentProfileService } from './ST-02-profile.service';

const profile: StudentProfileDto = {
  id: 7,
  full_name: 'Mai Nguyen',
  email: 'mai@example.com',
  role: 'STUDENT',
  status: 'ACTIVE',
  avatar_url: null,
  phone: null,
  created_at: '2026-01-01',
  updated_at: '2026-01-01',
};

describe('ST-02 profile cache', () => {
  it('reuses the profile for the same token and reloads after the token changes', async () => {
    let token = 'token-one';
    const getProfile = vi.fn(() => of(profile));
    TestBed.configureTestingModule({
      providers: [
        StudentProfileService,
        { provide: AuthSessionService, useValue: { ensureAccessToken: () => of(token) } },
        { provide: StudentAccountProfileService, useValue: { getProfile } },
      ],
    });
    const service = TestBed.inject(StudentProfileService);

    await firstValueFrom(service.getProfile());
    await firstValueFrom(service.getProfile());
    expect(getProfile).toHaveBeenCalledTimes(1);

    token = 'token-two';
    await firstValueFrom(service.getProfile());
    expect(getProfile).toHaveBeenCalledTimes(2);
  });

  it('does not retain a failed request', async () => {
    let fails = true;
    const getProfile = vi.fn(() => (fails ? throwError(() => new Error('offline')) : of(profile)));
    TestBed.configureTestingModule({
      providers: [
        StudentProfileService,
        { provide: AuthSessionService, useValue: { ensureAccessToken: () => of('token-one') } },
        { provide: StudentAccountProfileService, useValue: { getProfile } },
      ],
    });
    const service = TestBed.inject(StudentProfileService);

    await expect(firstValueFrom(service.getProfile())).rejects.toThrow('offline');
    fails = false;
    await expect(firstValueFrom(service.getProfile())).resolves.toEqual(profile);
    expect(getProfile).toHaveBeenCalledTimes(2);
  });
});
