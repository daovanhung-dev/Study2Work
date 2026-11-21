import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import type { StudentProfile } from '../../shared/models/student-api.models';
import { ST02ProfileService } from '../data-access/st02-profile.service';
import { ST02Page } from './st02-page';

describe('ST02Page', () => {
  it('shows the student profile and links to the supported edit screen', async () => {
    const data = { profile: vi.fn(() => of(envelope(profile))) };
    await TestBed.configureTestingModule({
      imports: [ST02Page],
      providers: [provideRouter([]), { provide: ST02ProfileService, useValue: data }],
    }).compileComponents();

    const fixture = TestBed.createComponent(ST02Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('h1')?.textContent?.trim()).toBe('Hồ sơ cá nhân');
    expect(root.textContent).toContain('Nguyễn An');
    expect(root.textContent).toContain('an@example.test');
    expect(root.textContent).toContain('Học viên');
    expect(root.textContent).toContain('Đang hoạt động');
    expect(root.querySelector('img')?.getAttribute('src')).toBe(profile.avatar_url);
    expect(root.querySelector('a[href="/student/profile/edit"]')).not.toBeNull();
    expect(data.profile).toHaveBeenCalledOnce();
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

function envelope<T>(data: T) {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Retrieved.',
    data,
    traceId: 'test-trace',
  };
}
