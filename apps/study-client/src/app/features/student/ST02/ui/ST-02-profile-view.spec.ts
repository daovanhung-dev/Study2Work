import { TestBed } from '@angular/core/testing';
import { describe, expect, it } from 'vitest';

import type { StudentProfileDto } from '../models/ST-02-profile.models';
import { StudentProfileView } from './ST-02-profile-view';

const profile: StudentProfileDto = {
  id: 7,
  full_name: 'Mai Nguyen',
  email: 'mai@example.com',
  role: 'STUDENT',
  status: 'ACTIVE',
  avatar_url: 'https://example.com/avatar.png',
  phone: null,
  created_at: '2026-01-01',
  updated_at: '2026-01-01',
};

describe('ST-02 profile view', () => {
  it('uses the profile avatar, falls back on image error and disables edit', async () => {
    await TestBed.configureTestingModule({ imports: [StudentProfileView] }).compileComponents();
    const fixture = TestBed.createComponent(StudentProfileView);
    fixture.componentRef.setInput('state', 'ready');
    fixture.componentRef.setInput('profile', profile);
    fixture.detectChanges();

    const avatar = fixture.nativeElement.querySelector('.avatar-circle img') as HTMLImageElement;
    expect(avatar.getAttribute('src')).toBe(profile.avatar_url);
    expect(avatar.getAttribute('alt')).toContain(profile.full_name);
    const edit = fixture.nativeElement.querySelector('.btn-muted') as HTMLButtonElement;
    expect(edit.disabled).toBe(true);

    avatar.dispatchEvent(new Event('error'));
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('.avatar-circle img')).toBeNull();
    expect(fixture.nativeElement.querySelector('.avatar-circle svg')).not.toBeNull();
  });

  it('shows the fallback icon when the API has no avatar URL', async () => {
    await TestBed.configureTestingModule({ imports: [StudentProfileView] }).compileComponents();
    const fixture = TestBed.createComponent(StudentProfileView);
    fixture.componentRef.setInput('state', 'ready');
    fixture.componentRef.setInput('profile', { ...profile, avatar_url: null });
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelector('.avatar-circle img')).toBeNull();
    expect(fixture.nativeElement.querySelector('.avatar-circle svg')).not.toBeNull();
  });
});
