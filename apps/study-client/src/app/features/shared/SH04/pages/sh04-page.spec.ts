import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { describe, expect, it } from 'vitest';

import { SH04Page } from './sh04-page';

describe('SH04Page', () => {
  it('explains the unavailable verification flow and provides a login route', async () => {
    await TestBed.configureTestingModule({
      imports: [SH04Page],
      providers: [provideRouter([])],
    }).compileComponents();

    const fixture = TestBed.createComponent(SH04Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[data-screen-id="SH-04"]')).not.toBeNull();
    expect(root.querySelector('h1')?.textContent?.trim()).toBe('Chưa thể xác minh email');
    expect(root.querySelector('[role="status"]')?.textContent).toContain(
      'không gửi email',
    );
    expect(root.textContent).toContain('không xác nhận trạng thái email của tài khoản');
    expect(root.querySelector('input, form, button')).toBeNull();
    expect(root.querySelector('a[href="/login"]')?.textContent).toContain('Quay lại đăng nhập');
  });
});
