import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { describe, expect, it } from 'vitest';

import { SystemNotFoundPage } from './SH-06-not-found-page';

describe('SH-06 not-found page', () => {
  it('does not report a failed API request as a missing resource', async () => {
    await TestBed.configureTestingModule({
      imports: [SystemNotFoundPage],
      providers: [
        {
          provide: Router,
          useValue: { getCurrentNavigation: () => ({ extras: { state: { httpError: { status: 500 } } } }) },
        },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(SystemNotFoundPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state.source).toBe('error');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Không thể tải tài nguyên');
  });
});
