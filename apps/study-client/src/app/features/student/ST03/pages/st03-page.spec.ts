import { TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import type { StudentProfile } from '../../shared/models/student-api.models';
import { ST03ProfileService } from '../data-access/st03-profile.service';
import { ST03Page } from './st03-page';

describe('ST03Page', () => {
  let data: {
    profile: ReturnType<typeof vi.fn>;
    uploadAvatar: ReturnType<typeof vi.fn>;
    updateProfile: ReturnType<typeof vi.fn>;
  };

  beforeEach(async () => {
    data = {
      profile: vi.fn(() => of(envelope(profile))),
      uploadAvatar: vi.fn(() => of(envelope({ avatar_url: profile.avatar_url }, 'DESIGN_RESOURCE_CREATED'))),
      updateProfile: vi.fn((update: Partial<StudentProfile>) =>
        of(envelope({ ...profile, ...update }, 'DESIGN_RESOURCE_UPDATED')),
      ),
    };
    await TestBed.configureTestingModule({
      imports: [ST03Page],
      providers: [provideRouter([]), { provide: ST03ProfileService, useValue: data }],
    }).compileComponents();
  });

  it('loads editable name and phone while keeping email read-only and bio disabled', () => {
    const fixture = TestBed.createComponent(ST03Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[data-screen-id="ST-03"]')).not.toBeNull();
    expect(root.querySelector<HTMLInputElement>('#st03-full-name')?.value).toBe(profile.full_name);
    expect(root.querySelector<HTMLInputElement>('#st03-phone')?.value).toBe(profile.phone);
    expect(root.querySelector<HTMLInputElement>('#st03-email')?.readOnly).toBe(true);
    expect(root.querySelector<HTMLTextAreaElement>('#st03-bio')?.disabled).toBe(true);
    expect(root.textContent).not.toContain('API #13');
    expect(root.textContent).not.toContain('API #14');
    expect(data.profile).toHaveBeenCalledOnce();
  });

  it('saves the supported profile fields and refreshes the profile', async () => {
    vi.spyOn(TestBed.inject(Router), 'navigate').mockResolvedValue(true);
    const fixture = TestBed.createComponent(ST03Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    const fullName = root.querySelector<HTMLInputElement>('#st03-full-name')!;
    const phone = root.querySelector<HTMLInputElement>('#st03-phone')!;
    fullName.value = 'Nguyễn An mới';
    fullName.dispatchEvent(new Event('input'));
    phone.value = '0912345678';
    phone.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    expect(root.querySelector<HTMLButtonElement>('.profile-edit-save')?.disabled).toBe(false);
    root.querySelector('form')!.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    await fixture.whenStable();

    expect(data.updateProfile).toHaveBeenCalledWith({
      full_name: 'Nguyễn An mới',
      phone: '0912345678',
      avatar_url: profile.avatar_url,
    });
    expect(data.profile).toHaveBeenCalledTimes(2);
  });

  it('rejects an empty name without sending an update', () => {
    const fixture = TestBed.createComponent(ST03Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    const fullName = root.querySelector<HTMLInputElement>('#st03-full-name')!;
    fullName.value = '   ';
    fullName.dispatchEvent(new Event('input'));
    root.querySelector('form')!.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    fixture.detectChanges();

    expect(data.updateProfile).not.toHaveBeenCalled();
    expect(root.textContent).toContain('Họ và tên phải có từ 1 đến 150 ký tự.');
  });
});

const profile: StudentProfile = {
  id: 5,
  full_name: 'Nguyễn An',
  email: 'an@example.test',
  role: 'STUDENT',
  avatar_url: 'https://cdn.example.test/avatar.png',
  phone: '0900000000',
  status: 'ACTIVE',
  created_at: '2026-11-20T09:00:00Z',
  updated_at: '2026-11-20T09:00:00Z',
};

function envelope<T>(data: T, businessCode = 'DESIGN_RESOURCE_RETRIEVED') {
  return {
    success: true,
    businessCode,
    message: 'Retrieved.',
    data,
    traceId: 'test-trace',
  };
}
