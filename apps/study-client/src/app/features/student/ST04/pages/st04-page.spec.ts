import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { provideRouter, Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { afterEach, describe, expect, it } from 'vitest';

import { ST04Page } from './st04-page';

describe('ST04Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ST04Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([{ path: 'student/enroll/:courseId', component: ST04Page }]),
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('loads the published course and keeps enrollment behind the unresolved identity gate', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/enroll/42', ST04Page);

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
            price: '0.00',
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
    expect(root.querySelector('[data-screen-id="ST-04"]')).not.toBeNull();
    expect(root.textContent).toContain('Kiểm tra ghi danh');
    expect(root.textContent).toContain('API #15 hiện chưa xác định enrollment');
    expect(root.textContent).not.toContain('Đã ghi danh');
    http.expectNone('/api/v1/courses/42/enrollment-status');
    expect(TestBed.inject(Router).url).toBe('/student/enroll/42');
  });

  it('shows the not-found state for an unavailable course without checking enrollment', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/enroll/999', ST04Page);

    http
      .expectOne('/api/v1/courses/999')
      .flush(
        { success: false, businessCode: 'DESIGN_RESOURCE_NOT_FOUND' },
        { status: 404, statusText: 'Not Found' },
      );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Không tìm thấy khóa học');
    http.expectNone('/api/v1/courses/999/enrollment-status');
  });
});
