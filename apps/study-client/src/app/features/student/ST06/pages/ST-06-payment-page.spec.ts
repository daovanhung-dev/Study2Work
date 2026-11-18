import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it } from 'vitest';

import { StudentPaymentPage } from './ST-06-payment-page';

describe('ST-06 payment page', () => {
  async function render(orderId?: string) {
    const paramMap = convertToParamMap(orderId === undefined ? {} : { orderId });
    await TestBed.configureTestingModule({
      imports: [StudentPaymentPage],
      providers: [{ provide: ActivatedRoute, useValue: { paramMap: of(paramMap), snapshot: { paramMap } } }],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentPaymentPage);
    fixture.detectChanges();
    return fixture;
  }

  it('rejects a missing order ID without claiming a payment status', async () => {
    const fixture = await render();
    expect(fixture.componentInstance.state().kind).toBe('missing-context');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Mã đơn hàng không hợp lệ');
  });

  it('rejects a malformed order ID', async () => {
    const fixture = await render('abc');
    expect(fixture.componentInstance.state().kind).toBe('missing-context');
  });

  it('shows the truthful provider gate for a valid ID and matches DD card semantics', async () => {
    const fixture = await render('1');
    const element = fixture.nativeElement as HTMLElement;

    expect(fixture.componentInstance.state().kind).toBe('blocked');
    expect(element.textContent).toContain('Cổng thanh toán hiện chưa được cấu hình');
    expect(element.textContent).toContain('Kiểm tra đơn hàng');
    expect(element.querySelector('.icon-circle svg')).not.toBeNull();
    expect(element.querySelector<HTMLAnchorElement>('.btn-primary')?.getAttribute('href')).toBe('/student/courses');
    expect(element.textContent).not.toContain('Đã thanh toán');
  });

  it('rejects values outside the int64 order ID range', async () => {
    const fixture = await render('9223372036854775808');
    expect(fixture.componentInstance.state().kind).toBe('missing-context');
  });
});
