import { HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { describe, expect, it } from 'vitest';

import { SH05Page } from './sh05-page';

describe('SH05Page', () => {
  it('presents the safe 401 message and trace without claiming the session expired', async () => {
    await TestBed.configureTestingModule({ imports: [SH05Page], providers: [provideRouter([])] }).compileComponents();

    const fixture = TestBed.createComponent(SH05Page);
    fixture.componentRef.setInput(
      'errorResponse',
      errorResponse(401, 'DESIGN_AUTHENTICATION_REQUIRED', 'Authentication required.', 'trace-401'),
    );
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[data-screen-id="SH-05"]')).not.toBeNull();
    expect(root.querySelector('h1')?.textContent?.trim()).toBe('Không thể xác thực yêu cầu');
    expect(root.querySelector('[role="status"]')?.textContent).toContain(
      'Authentication required.',
    );
    expect(root.textContent?.toLowerCase()).not.toContain('expired');
    expect(root.querySelector('study-sh05-trace-card code')?.textContent).toBe('trace-401');
    expect(root.querySelector('a.error-card__back')?.getAttribute('href')).toBe('/');
  });

  it('does not render invalid or mismatched error context', async () => {
    await TestBed.configureTestingModule({ imports: [SH05Page], providers: [provideRouter([])] }).compileComponents();

    const fixture = TestBed.createComponent(SH05Page);
    fixture.componentRef.setInput(
      'errorResponse',
      errorResponse(401, 'DESIGN_ACCESS_DENIED', 'Access denied.', 'trace-wrong'),
    );
    fixture.detectChanges();

    expect(
      (fixture.nativeElement as HTMLElement).querySelector('[data-screen-id="SH-05"]'),
    ).toBeNull();
  });
});

function errorResponse(
  status: number,
  businessCode: string,
  message: string,
  traceId: string,
): HttpErrorResponse {
  return new HttpErrorResponse({
    status,
    headers: new HttpHeaders({ 'X-Trace-Id': traceId }),
    error: { success: false, businessCode, message, traceId, data: null, meta: {} },
  });
}
