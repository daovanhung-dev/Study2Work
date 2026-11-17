import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { describe, expect, it } from 'vitest';

import { ST07Page } from './st07-page';

describe('ST07Page', () => {
  it('shows the unavailable enrollment result instead of inferring success', async () => {
    await TestBed.configureTestingModule({
      imports: [ST07Page],
      providers: [provideRouter([])],
    }).compileComponents();
    const fixture = TestBed.createComponent(ST07Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[data-screen-id="ST-07"]')).not.toBeNull();
    expect(root.textContent).toContain('Chưa thể xác nhận kết quả đăng ký.');
    expect(root.textContent).not.toContain('Đăng ký thành công');
    expect(root.querySelector('a[href="/student/courses"]')).not.toBeNull();
  });
});
