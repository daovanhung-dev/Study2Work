import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { describe, expect, it } from 'vitest';

import { SystemForbiddenPage } from './SH-05-forbidden-page';

describe('SH-05 forbidden page', () => {
  it('distinguishes a verified 403 handoff from an unknown access failure', async () => {
    await TestBed.configureTestingModule({
      imports: [SystemForbiddenPage],
      providers: [
        {
          provide: Router,
          useValue: { getCurrentNavigation: () => ({ extras: { state: { httpError: { status: 403, traceId: 'trace-403' } } } }) },
        },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(SystemForbiddenPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state.status).toBe(403);
    expect(fixture.componentInstance.state.traceId).toBe('trace-403');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Không đủ quyền');
  });
});
