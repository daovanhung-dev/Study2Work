import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { describe, expect, it } from 'vitest';

import { SH06Page } from './sh06-page';

describe('SH06Page', () => {
  it('renders a minimal 404 with the supported course and home routes', async () => {
    await TestBed.configureTestingModule({
      imports: [SH06Page],
      providers: [provideRouter([])],
    }).compileComponents();

    const fixture = TestBed.createComponent(SH06Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;

    expect(root.querySelector('[data-screen-id="SH-06"]')).not.toBeNull();
    expect(root.querySelector('.not-found__code')?.textContent?.trim()).toBe('404');
    expect(root.querySelector('a[href="/courses"]')?.textContent).toContain('Danh sách khóa học');
    expect(root.querySelector('.not-found__action--secondary')?.getAttribute('href')).toBe('/');
    expect(root.querySelector('.not-found__action--secondary')?.textContent).toContain('Về trang chủ');
    expect(root.textContent).not.toContain('403');
    expect(root.querySelectorAll('a[href="#"]')).toHaveLength(0);
  });
});
