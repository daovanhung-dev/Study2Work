import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { describe, expect, it } from 'vitest';

import { GS07Page } from './gs07-page';

describe('GS07Page', () => {
  it('renders an accessible gate notice without resource identifiers or actions', async () => {
    await TestBed.configureTestingModule({
      imports: [GS07Page],
      providers: [provideRouter([])],
    }).compileComponents();
    const fixture = TestBed.createComponent(GS07Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const main = root.querySelector('main[data-screen-id="GS07"]');
    const status = main?.querySelector('[role="status"]');
    expect(status?.getAttribute('aria-labelledby')).toBe('gs07-status-heading');
    expect(status?.textContent).toContain('Chưa thể mở tài nguyên này');
    expect(status?.textContent).toContain('Hiện chưa thể hiển thị hoặc tải tài nguyên này.');
    expect(main?.querySelector('a, button, iframe, video, object, embed')).toBeNull();
  });
});
