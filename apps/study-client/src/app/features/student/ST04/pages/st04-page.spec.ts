import { HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of, throwError } from 'rxjs';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { GS03CourseDetailService } from '../../../guest/GS03/data-access/gs03-course-detail.service';
import { ST04EnrollmentService } from '../data-access/st04-enrollment.service';
import { ST04Page } from './st04-page';

@Component({ standalone: true, template: '' })
class EmptyRoute {}

describe('ST04Page', () => {
  let courseDetail: { getCourse: ReturnType<typeof vi.fn> };
  let enrollment: {
    enrollmentStatus: ReturnType<typeof vi.fn>;
    enroll: ReturnType<typeof vi.fn>;
    courses: ReturnType<typeof vi.fn>;
  };

  beforeEach(async () => {
    courseDetail = { getCourse: vi.fn(() => of(courseEnvelope('0.00'))) };
    enrollment = {
      enrollmentStatus: vi.fn(() => of(envelope({
        id: 3,
        course_id: 42,
        user_id: 5,
        status: 'ACTIVE',
        enrolled_at: '2026-11-20T09:00:00Z',
      }))),
      enroll: vi.fn(() => of(envelope({
        id: 3,
        course_id: 42,
        user_id: 5,
        status: 'ACTIVE',
        enrolled_at: '2026-11-20T09:00:00Z',
      }, 'DESIGN_RESOURCE_CREATED'))),
      courses: vi.fn(() => of(envelope({
        items: [{
          course_id: 42,
          name: 'Khóa học miễn phí',
          enrollment_status: 'ACTIVE',
          enrolled_at: '2026-11-20T09:00:00Z',
        }],
        pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
      }))),
    };

    await TestBed.configureTestingModule({
      imports: [ST04Page],
      providers: [
        provideRouter([
          { path: 'student/enroll/:courseId', component: ST04Page },
          { path: 'student/courses', component: EmptyRoute },
          { path: 'student/checkout/:courseId', component: EmptyRoute },
          { path: 'courses', component: EmptyRoute },
          { path: 'login', component: EmptyRoute },
        ]),
        { provide: GS03CourseDetailService, useValue: courseDetail },
        { provide: ST04EnrollmentService, useValue: enrollment },
      ],
    }).compileComponents();
  });

  it('recognizes an active enrollment and does not send another enrollment request', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/enroll/42', ST04Page);
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Bạn đã ghi danh khóa học');
    expect(root.querySelector('a[href="/student/courses"]')).not.toBeNull();
    expect(enrollment.enroll).not.toHaveBeenCalled();
    expect(enrollment.enrollmentStatus).toHaveBeenCalledWith('42');
  });

  it('enrolls a free course only after a not-enrolled response and confirms it in my courses', async () => {
    enrollment.enrollmentStatus.mockReturnValueOnce(
      throwError(() => new HttpErrorResponse({ status: 404, statusText: 'Not Found' })),
    );
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/enroll/42', ST04Page);
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const button = Array.from(root.querySelectorAll('button')).find((item) =>
      item.textContent?.includes('Đăng ký miễn phí'),
    );
    expect(button).toBeTruthy();
    button!.click();
    await harness.fixture.whenStable();

    expect(enrollment.enroll).toHaveBeenCalledWith(42);
    expect(enrollment.courses).toHaveBeenCalledOnce();
    expect(TestBed.inject(Router).url).toBe('/student/courses');
  });

  it('keeps paid courses out of enrollment and routes to the gated checkout screen', async () => {
    courseDetail.getCourse.mockReturnValueOnce(of(courseEnvelope('25.00')));
    enrollment.enrollmentStatus.mockReturnValueOnce(
      throwError(() => new HttpErrorResponse({ status: 404, statusText: 'Not Found' })),
    );
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/enroll/42', ST04Page);
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Khóa học này có học phí');
    expect(root.querySelector('a[href="/student/checkout/42"]')).not.toBeNull();
    expect(enrollment.enroll).not.toHaveBeenCalled();
  });
});

function courseEnvelope(price: string) {
  return envelope({
    items: [{
      id: 42,
      title: 'Khóa học miễn phí',
      description: null,
      thumbnail_url: null,
      price,
      status: 'PUBLISHED',
      mentor: { id: 2, full_name: 'Mentor', avatar_url: null },
    }],
    pagination: { page: 1, size: 1, total: 1, total_pages: 1 },
  });
}

function envelope<T>(data: T, businessCode = 'DESIGN_RESOURCE_RETRIEVED') {
  return {
    success: true,
    businessCode,
    message: 'Retrieved.',
    data,
    traceId: 'test-trace',
  };
}
