import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { describe, expect, it } from 'vitest';

import { StudentProfileService } from '../data-access/ST-02-profile.service';
import { StudentProfilePage } from './ST-02-profile-page';

describe('ST-02 profile page', () => {
  it('shows the profile returned by the API', async () => {
    const profile = { id: 7, full_name: 'Mai Nguyen', email: 'mai@example.com', role: 'student', avatar_url: null, phone: null, status: 'active', created_at: '2026-01-01', updated_at: '2026-01-01' };
    await TestBed.configureTestingModule({
      imports: [StudentProfilePage],
      providers: [{ provide: StudentProfileService, useValue: { getProfile: () => of(profile) } }],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentProfilePage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state()).toBe('ready');
    expect(fixture.componentInstance.profile()).toEqual(profile);
  });

  it('shows unauthorized state when profile API returns 401', async () => {
    await TestBed.configureTestingModule({
      imports: [StudentProfilePage],
      providers: [
        { provide: StudentProfileService, useValue: { getProfile: () => throwError(() => new HttpErrorResponse({ status: 401 })) } },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentProfilePage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state()).toBe('unauthorized');
    expect(fixture.componentInstance.profile()).toBeNull();
  });
});
