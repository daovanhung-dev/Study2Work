import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { describe, expect, it } from 'vitest';

import { ST08Page } from './st08-page';

describe('ST08Page', () => {
  it('renders the documented empty-list state without mock courses or progress', async () => {
    await TestBed.configureTestingModule({
      imports: [ST08Page],
      providers: [provideRouter([])],
    }).compileComponents();
    const fixture = TestBed.createComponent(ST08Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[data-screen-id="ST-08"]')).not.toBeNull();
    expect(root.textContent).toContain('Chưa có khóa học để hiển thị.');
    expect(root.querySelectorAll('[data-course-id]')).toHaveLength(0);
    expect(root.textContent).not.toContain('%');
  });
});
