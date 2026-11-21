import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { afterEach, describe, expect, it } from 'vitest';

import { ST05Page } from './st05-page';

describe('ST05Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ST05Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([{ path: 'student/checkout/:courseId', component: ST05Page }]),
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('revalidates a published course and keeps order creation unavailable', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/checkout/42', ST05Page);

    const courseRequest = http.expectOne('/api/v1/courses/42');
    expect(courseRequest.request.method).toBe('GET');
    expect(courseRequest.request.headers.has('Authorization')).toBe(false);
    courseRequest.flush({
      success: true,
      businessCode: 'DESIGN_RESOURCE_RETRIEVED',
      message: 'Course retrieved.',
      data: {
        items: [
          {
            id: 42,
            title: 'Khóa học công khai',
            description: null,
            thumbnail_url: null,
            price: '125000.00',
            status: 'PUBLISHED',
            mentor: { id: 2, full_name: 'Mentor', avatar_url: null },
          },
        ],
        pagination: { page: 1, size: 1, total: 1, total_pages: 1 },
      },
      traceId: 'test-trace-id',
    });
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('[data-screen-id="ST-05"]')).not.toBeNull();
    expect(root.textContent).toContain('Quy trình thanh toán chưa thể bắt đầu.');
    expect(root.textContent).toContain('Vui lòng kiểm tra lại điều kiện ghi danh.');
    expect(root.textContent).not.toContain('125000.00');
    http.expectNone('/api/v1/orders');
    expect(TestBed.inject(Router).url).toBe('/student/checkout/42');
  });

  it('keeps the not-found state separate from order availability', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/checkout/999', ST05Page);

    http
      .expectOne('/api/v1/courses/999')
      .flush(
        { success: false, businessCode: 'DESIGN_RESOURCE_NOT_FOUND' },
        { status: 404, statusText: 'Not Found' },
      );
    harness.fixture.detectChanges();

    expect((harness.routeNativeElement as HTMLElement).textContent).toContain(
      'Không tìm thấy khóa học',
    );
    http.expectNone('/api/v1/orders');
  });
});
