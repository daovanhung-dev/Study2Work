import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { MentorSessionService } from '../../../../core/auth/mentor-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { MentorCourse, MentorPage } from '../../shared/models/mentor-api.models';
import { ME02Page } from './me02-page';

describe('ME02Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ME02Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([{ path: 'mentor/courses', component: ME02Page }]),
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('loads authenticated API #46 data and renders only supported course fields', async () => {
    signInAsMentor();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/mentor/courses', ME02Page);
    const root = harness.routeNativeElement!;

    expect(page.loading()).toBe(true);
    expect(root.querySelector('[role="status"]')?.textContent).toContain('Đang tải khóa học');
    const request = expectCoursesRequest({ page: '1', size: '20' });
    expect(request.request.headers.get('Authorization')).toBe('Bearer mentor-access-token');
    expect(request.request.body).toBeNull();
    request.flush(successEnvelope(coursePage([course()], 1, 1, 1)));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(page.loading()).toBe(false);
    expect(root.querySelector('h2')?.textContent).toContain('English Basics');
    expect(root.textContent).toContain('Owned course description.');
    expect(root.textContent).toContain('Mentor One');
    expect(root.textContent).toContain('Bản nháp');
    expect(root.textContent).toContain('ID #7');
    expect(root.textContent).toContain('Chưa có ảnh xem trước');
    expect(root.textContent).not.toContain('10.00');
    expect(root.querySelector('input')).toBeNull();
    expect(root.querySelector('a[href="/mentor/courses/7"]')?.textContent).toContain('Mở workspace');
    expect(root.querySelector('[aria-label="Phân trang khóa học"]')).not.toBeNull();
  });

  it('resets pagination and sends only the approved status filter to API #46', async () => {
    signInAsMentor();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/mentor/courses', ME02Page);
    expectCoursesRequest({ page: '1', size: '20' }).flush(
      successEnvelope(coursePage([course()], 1, 21, 2)),
    );
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const select = harness.routeNativeElement?.querySelector<HTMLSelectElement>('#me02-status');
    if (!select) throw new Error('ME-02 status filter is missing.');
    select.value = 'PUBLISHED';
    select.dispatchEvent(new Event('change', { bubbles: true }));
    harness.fixture.detectChanges();

    expect(page.page()).toBe(1);
    expect(page.status()).toBe('PUBLISHED');
    const request = expectCoursesRequest({ page: '1', size: '20', status: 'PUBLISHED' });
    expect(request.request.params.keys().sort()).toEqual(['page', 'size', 'status']);
    request.flush(successEnvelope(coursePage([course(8, 'PUBLISHED')], 1, 1, 1)));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(harness.routeNativeElement?.querySelector('.me02-course-status')?.textContent).toContain(
      'Đã xuất bản',
    );
    expect(harness.routeNativeElement?.querySelector('.me02-course-status')?.textContent).not.toContain(
      'Bản nháp',
    );
  });

  it('recovers an empty out-of-range page and shows the server-backed empty state', async () => {
    signInAsMentor();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/mentor/courses', ME02Page);
    expectCoursesRequest({ page: '1', size: '20' }).flush(
      successEnvelope(coursePage([course()], 1, 21, 2)),
    );
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const nextButton = Array.from(
      harness.routeNativeElement?.querySelectorAll<HTMLButtonElement>(
        'nav[aria-label="Phân trang khóa học"] button',
      ) ?? [],
    ).find((button) => button.textContent?.includes('Trang sau'));
    if (!nextButton) throw new Error('ME-02 next-page button is missing.');
    nextButton.click();
    harness.fixture.detectChanges();
    const outOfRange = expectCoursesRequest({ page: '2', size: '20' });
    outOfRange.flush(successEnvelope(coursePage([], 2, 0, 0)));

    const recovered = expectCoursesRequest({ page: '1', size: '20' });
    recovered.flush(successEnvelope(coursePage([], 1, 0, 0)));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(page.page()).toBe(1);
    expect(page.total()).toBe(0);
    expect(harness.routeNativeElement?.textContent).toContain('Chưa có khóa học');
    expect(harness.routeNativeElement?.querySelector('[role="alert"]')).toBeNull();
  });

  it('rejects an invalid Course projection and does not render it as loaded data', async () => {
    signInAsMentor();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/mentor/courses', ME02Page);
    const invalidCourse = { ...course(), id: '7' } as unknown as MentorCourse;
    expectCoursesRequest({ page: '1', size: '20' }).flush(
      successEnvelope(coursePage([invalidCourse], 1, 1, 1)),
    );
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(page.error()).toContain('dữ liệu khóa học không hợp lệ');
    expect(harness.routeNativeElement?.querySelector('.me02-course-list')).toBeNull();
    expect(harness.routeNativeElement?.querySelector('[role="alert"]')).not.toBeNull();
  });

  it('keeps an HTTP failure separate from loaded data and retries API #46 on request', async () => {
    signInAsMentor();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/mentor/courses', ME02Page);
    expectCoursesRequest({ page: '1', size: '20' }).flush(
      {
        success: false,
        businessCode: 'DESIGN_INTERNAL_ERROR',
        message: 'failed',
        data: null,
        meta: {},
        traceId: 'me02-http-error',
      },
      { status: 500, statusText: 'Server Error' },
    );
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement!;
    expect(page.error()).not.toBeNull();
    expect(root.querySelector('.me02-course-list')).toBeNull();
    expect(root.querySelector('[role="alert"]')?.textContent).toContain('failed');

    root.querySelector<HTMLButtonElement>('[role="alert"] button')?.click();
    harness.fixture.detectChanges();
    const retry = expectCoursesRequest({ page: '1', size: '20' });
    expect(retry.request.headers.get('Authorization')).toBe('Bearer mentor-access-token');
    retry.flush(successEnvelope(coursePage([course()], 1, 1, 1)));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(page.error()).toBeNull();
    expect(root.textContent).toContain('English Basics');
  });

  function expectCoursesRequest(params: Record<string, string>) {
    const request = http.expectOne((candidate) => candidate.url === '/api/v1/mentor/courses');
    expect(request.request.method).toBe('GET');
    expect(request.request.params.keys().sort()).toEqual(Object.keys(params).sort());
    for (const [key, value] of Object.entries(params)) {
      expect(request.request.params.get(key)).toBe(value);
    }
    return request;
  }

  function signInAsMentor(): void {
    TestBed.inject(MentorSessionService).acceptLoginEnvelope(
      successEnvelope({
        full_name: 'Mentor One',
        email: 'mentor@example.test',
        role: 'MENTOR',
        access_token: 'mentor-access-token',
        refresh_token: 'mentor-refresh-token',
        token_type: 'bearer',
        expires_in: 3600,
        refresh_expires_in: 7200,
      }),
    );
  }
});

function successEnvelope<T>(
  data: T,
  businessCode = 'DESIGN_RESOURCE_RETRIEVED',
): ApiEnvelope<T> {
  return {
    success: true,
    businessCode,
    message: 'ok',
    data,
    meta: {},
    traceId: 'me02-test',
  };
}

function coursePage(
  items: MentorCourse[],
  page: number,
  total: number,
  totalPages: number,
): MentorPage<MentorCourse> {
  return { items, pagination: { page, size: 20, total, total_pages: totalPages } };
}

function course(id = 7, status: 'DRAFT' | 'PUBLISHED' = 'DRAFT'): MentorCourse {
  return {
    id,
    title: 'English Basics',
    description: 'Owned course description.',
    thumbnail_url: null,
    price: '10.00',
    status,
    mentor: { id: 5, full_name: 'Mentor One', avatar_url: null },
  };
}
