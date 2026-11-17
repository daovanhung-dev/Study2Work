import { TestBed } from '@angular/core/testing';
import { describe, expect, it } from 'vitest';

import { GS06Page } from './gs06-page';

describe('GS06Page', () => {
  it('renders an accessible unavailable state without resource actions', async () => {
    await TestBed.configureTestingModule({ imports: [GS06Page] }).compileComponents();
    const fixture = TestBed.createComponent(GS06Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const status = root.querySelector('[role="status"]');
    expect(status?.textContent).toContain('Tài nguyên hiện chưa khả dụng');
    expect(status?.textContent).toContain('Hiện chưa thể hiển thị hoặc mở tài nguyên');
    expect(root.querySelector('a, button')).toBeNull();
  });
});
