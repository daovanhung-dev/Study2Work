import { TestBed } from '@angular/core/testing';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { SH05TraceCard } from './sh05-trace-card';

describe('SH05TraceCard', () => {
  const originalClipboard = Object.getOwnPropertyDescriptor(navigator, 'clipboard');

  afterEach(() => {
    if (originalClipboard) {
      Object.defineProperty(navigator, 'clipboard', originalClipboard);
    } else {
      Reflect.deleteProperty(navigator, 'clipboard');
    }
  });

  it('copies only the supplied trace ID and announces success', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, 'clipboard', {
      configurable: true,
      value: { writeText },
    });
    await TestBed.configureTestingModule({ imports: [SH05TraceCard] }).compileComponents();

    const fixture = TestBed.createComponent(SH05TraceCard);
    fixture.componentRef.setInput('traceId', 'trace-real-401');
    fixture.detectChanges();
    (fixture.nativeElement as HTMLElement).querySelector('button')?.click();
    await fixture.whenStable();
    fixture.detectChanges();

    expect(writeText).toHaveBeenCalledOnce();
    expect(writeText).toHaveBeenCalledWith('trace-real-401');
    expect(
      (fixture.nativeElement as HTMLElement).querySelector('[role="status"]')?.textContent,
    ).toContain('Đã sao chép Trace ID.');
  });

  it('announces clipboard rejection and leaves the trace text selectable', async () => {
    const writeText = vi.fn().mockRejectedValue(new Error('clipboard denied'));
    Object.defineProperty(navigator, 'clipboard', {
      configurable: true,
      value: { writeText },
    });
    await TestBed.configureTestingModule({ imports: [SH05TraceCard] }).compileComponents();

    const fixture = TestBed.createComponent(SH05TraceCard);
    fixture.componentRef.setInput('traceId', 'trace-real-403');
    fixture.detectChanges();
    (fixture.nativeElement as HTMLElement).querySelector('button')?.click();
    await fixture.whenStable();
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[role="status"]')?.textContent).toContain('sao chép thủ công');
    expect(root.querySelector('code')?.textContent).toBe('trace-real-403');
  });
});
