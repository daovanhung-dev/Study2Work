import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { describe, expect, it } from 'vitest';

import { StudentProfileEditService } from '../data-access/ST-03-profile-edit.service';
import { StudentProfileEditPage } from './ST-03-profile-edit-page';

describe('ST-03 profile edit page', () => {
  it('loads editable profile data from the API', async () => {
    const profile = { id: 7, full_name: 'Mai Nguyen', email: 'mai@example.com', role: 'student', avatar_url: null, phone: null, status: 'active', created_at: '2026-01-01', updated_at: '2026-01-01' };
    await TestBed.configureTestingModule({
      imports: [StudentProfileEditPage],
      providers: [{ provide: StudentProfileEditService, useValue: { getProfile: () => of(profile) } }],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentProfileEditPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state()).toBe('ready');
    expect(fixture.componentInstance.profile()).toEqual(profile);
  });

  it('blocks editing when the profile API returns 403', async () => {
    await TestBed.configureTestingModule({
      imports: [StudentProfileEditPage],
      providers: [
        { provide: StudentProfileEditService, useValue: { getProfile: () => throwError(() => new HttpErrorResponse({ status: 403 })) } },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentProfileEditPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state()).toBe('forbidden');
    expect(fixture.componentInstance.profile()).toBeNull();
  });
});
