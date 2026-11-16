import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AD24Page } from './ad24-page';

describe('AD24Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AD24Page],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('shows the unavailable report source and leaves the date and segment filters blank and disabled', () => {
    const fixture = TestBed.createComponent(AD24Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const dates = [...root.querySelectorAll<HTMLInputElement>('input[type="date"]')];
    expect(dates).toHaveLength(2);
    expect(dates.every((input) => input.value === '' && input.matches(':disabled'))).toBe(true);
    const segment = root.querySelector<HTMLSelectElement>('#report-segment');
    expect(segment?.value).toBe('');
    expect(segment?.matches(':disabled')).toBe(true);
    expect(root.textContent).toContain('Study Server chưa có route/query/model cho API #101 hoặc #102');
    expect(root.querySelector('.chart-unavailable')?.textContent).toContain('Không có chuỗi dữ liệu');
    expect(root.querySelectorAll('.metric-card')).toHaveLength(0);
    expect(root.querySelector('canvas, svg.chart')).toBeNull();
    http.expectNone((request) => request.url.includes('/admin/reports'));
  });

  it('keeps apply, reset, refresh and export disabled without a route to AD-25', () => {
    const fixture = TestBed.createComponent(AD24Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const actions = [...root.querySelectorAll<HTMLButtonElement>('button')];
    expect(actions).toHaveLength(4);
    expect(actions.every((button) => button.disabled)).toBe(true);
    expect(root.querySelector('a[href="/admin/reports/export"]')).toBeNull();
    expect(root.querySelector('a[href="/admin"]')).not.toBeNull();
    http.expectNone((request) => request.url.includes('/admin/reports'));
  });
});
