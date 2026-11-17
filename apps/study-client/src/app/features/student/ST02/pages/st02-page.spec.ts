import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { describe, expect, it } from 'vitest';

import { ST02Page } from './st02-page';

describe('ST02Page', () => {
  it('renders the documented sign-in gate and real navigation targets', async () => {
    await TestBed.configureTestingModule({
      imports: [ST02Page],
      providers: [provideRouter([])],
    }).compileComponents();

    const fixture = TestBed.createComponent(ST02Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[data-screen-id="ST-02"]')).not.toBeNull();
    expect(root.querySelector('h1')?.textContent?.trim()).toBe('Hồ sơ cá nhân');
    expect(root.querySelector('[role="status"]')?.textContent).toContain(
      'đăng nhập bằng tài khoản học viên',
    );
    expect(root.querySelector('a[href="/login"]')?.textContent).toContain('Đăng nhập');
    expect(root.querySelector('a[href="/"]')).not.toBeNull();
    expect(root.querySelector('a[href="/courses"]')).not.toBeNull();

    const editButton = root.querySelector<HTMLButtonElement>('button');
    expect(editButton?.disabled).toBe(true);
    expect(editButton?.textContent).toContain('Chỉnh sửa hồ sơ (Tạm khóa)');
    expect(root.textContent).not.toContain('permissions');
    expect(root.textContent).not.toContain('bio');
  });
});
