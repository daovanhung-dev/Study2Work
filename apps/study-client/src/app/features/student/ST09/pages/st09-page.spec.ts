import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { describe, expect, it } from 'vitest';

import { ST09Page } from './st09-page';

describe('ST09Page', () => {
  it('keeps course content and progress gated and renders no sample lessons', async () => {
    await TestBed.configureTestingModule({
      imports: [ST09Page],
      providers: [provideRouter([])],
    }).compileComponents();
    const fixture = TestBed.createComponent(ST09Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[data-screen-id="ST-09"]')).not.toBeNull();
    expect(root.textContent).toContain('Không tải dữ liệu giả định.');
    expect(root.textContent).toContain('API #09 chỉ trả đề cương công khai.');
    expect(root.querySelectorAll('[data-lesson-id]')).toHaveLength(0);
  });
});
