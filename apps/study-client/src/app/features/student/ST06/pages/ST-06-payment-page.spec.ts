import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it } from 'vitest';

import { StudentPaymentPage } from './ST-06-payment-page';

describe('ST-06 payment page', () => {
  it('does not claim payment information without an orderId', async () => {
    const paramMap = convertToParamMap({});
    await TestBed.configureTestingModule({
      imports: [StudentPaymentPage],
      providers: [{ provide: ActivatedRoute, useValue: { paramMap: of(paramMap), snapshot: { paramMap } } }],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentPaymentPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state().kind).toBe('missing-context');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Thiếu thông tin');
  });
});
