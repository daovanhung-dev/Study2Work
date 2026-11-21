import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { beforeEach, describe, expect, it } from 'vitest';

import { AD25Page } from './ad25-page';

describe('AD25Page', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AD25Page],
      providers: [provideRouter([])],
    }).compileComponents();
  });

  it('keeps format, scope and period selections local and leaves export unavailable', () => {
    const fixture = TestBed.createComponent(AD25Page);
    const page = fixture.componentInstance;

    expect(page.selectedFormat()).toBe('csv');
    expect(page.selectedScopes()).toEqual({ course: true, learner: true, impact: false });
    expect(page.selectedPeriod()).toBe('month');

    page.setFormat('pdf');
    page.setScope('impact', true);
    page.setPeriod('custom');
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(page.selectedFormat()).toBe('pdf');
    expect(page.selectedScopes().impact).toBe(true);
    expect(page.selectedPeriod()).toBe('custom');
    expect(root.querySelector('.format-option--selected strong')?.textContent).toContain('PDF');
    expect(root.querySelector('.config-submit button')?.hasAttribute('disabled')).toBe(true);
    expect(root.querySelector('.download-placeholder button')?.hasAttribute('disabled')).toBe(true);
    expect(root.textContent).toContain('chưa được gửi tới server');
  });
});
