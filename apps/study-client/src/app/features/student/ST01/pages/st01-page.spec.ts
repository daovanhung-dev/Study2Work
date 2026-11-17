import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { describe, expect, it } from 'vitest';

import { ST01Page } from './st01-page';

describe('ST01Page', () => {
  it('renders a Student session gate without sample dashboard metrics', async () => {
    await TestBed.configureTestingModule({
      imports: [ST01Page],
      providers: [provideRouter([])],
    }).compileComponents();
    const fixture = TestBed.createComponent(ST01Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[data-screen-id="ST-01"]')).not.toBeNull();
    expect(root.textContent).toContain('Đăng nhập để xem tổng quan học tập');
    expect(root.querySelector('a[href="/login"]')).not.toBeNull();
    expect(root.querySelectorAll('[data-metric]')).toHaveLength(0);
  });
});
