import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it } from 'vitest';

import { SystemOperationsPage } from './SH-07-operations-page';

describe('SH-07 operations page', () => {
  it('does not invent an operation when the route has no operationId', async () => {
    const paramMap = convertToParamMap({});
    await TestBed.configureTestingModule({
      imports: [SystemOperationsPage],
      providers: [{ provide: ActivatedRoute, useValue: { paramMap: of(paramMap), snapshot: { paramMap } } }],
    }).compileComponents();

    const fixture = TestBed.createComponent(SystemOperationsPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state().kind).toBe('missing-context');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Thiếu thông tin');
  });
});
