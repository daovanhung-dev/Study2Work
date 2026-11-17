import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { describe, expect, it } from 'vitest';

import { ST06Page } from './st06-page';

describe('ST06Page', () => {
  it('renders the Stitch unavailable state without starting or polling payment', async () => {
    await TestBed.configureTestingModule({
      imports: [ST06Page],
      providers: [provideRouter([{ path: 'student/pay/:orderId', component: ST06Page }])],
    }).compileComponents();

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/pay/42', ST06Page);
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('[data-screen-id="ST-06"]')).not.toBeNull();
    expect(root.textContent).toContain('Chưa có thông tin thanh toán để hiển thị.');
    expect(root.textContent).not.toContain('đã thanh toán');
    expect(root.querySelectorAll('button')).toHaveLength(0);
  });
});
