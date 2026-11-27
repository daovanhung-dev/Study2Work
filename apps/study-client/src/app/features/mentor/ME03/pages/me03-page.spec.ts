import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { MentorSessionService } from '../../../../core/auth/mentor-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type {
  MentorContent,
  MentorCourse,
  MentorCourseProgressRow,
  MentorPage,
} from '../../shared/models/mentor-api.models';
import { ME03Page } from './me03-page';

describe('ME03Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ME03Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([{ path: 'mentor/courses/:courseId', component: ME03Page }]),
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('loads authenticated #46/#49/#65 requests and renders supported workspace data', async () => {
    signInAsMentor();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/mentor/courses/7', ME03Page);
    const root = harness.routeNativeElement!;

    expect(page.loadingContent()).toBe(true);
    expect(page.loadingProgress()).toBe(true);
    expect(root.textContent).toContain('Đang tải nội dung');
    expect(root.textContent).toContain('Đang tải tiến độ');

    const coursesRequest = expectGet('/api/v1/mentor/courses');
    const contentRequest = expectGet('/api/v1/mentor/courses/7/content');
    const progressRequest = expectGet('/api/v1/mentor/courses/7/progress');
    coursesRequest.flush(successEnvelope(coursePage([course()], 1, 20, 1)));
    contentRequest.flush(successEnvelope([content(81, null, 'Unit A'), content(82, 81, 'Lesson 1') ]));
    progressRequest.flush(successEnvelope(progressPage([progressRow()])));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(page.courseTitle()).toBe('English Basics');
    expect(page.content().map((row) => row.title)).toEqual(['Unit A', 'Lesson 1']);
    expect(page.progress()).toHaveLength(1);
    expect(root.textContent).toContain('English Basics');
    expect(root.textContent).toContain('Unit A');
    expect(root.textContent).toContain('Lesson 1');
    expect(root.textContent).toContain('Student One');
    expect(root.textContent).toContain('2 / 3');
    expect(root.textContent).toContain('66%');
    expect(root.querySelector('[role="progressbar"]')?.getAttribute('aria-valuenow')).toBe('66');
    expect(root.querySelector('a[href="/mentor/courses/7/lectures/new"]')).not.toBeNull();
    expect(root.querySelector('a[href="/mentor/courses/7/content"]')).not.toBeNull();
    expect(root.querySelector('a[href="/mentor/courses/7/progress"]')).not.toBeNull();
    expect(root.querySelector('a[href="/mentor/courses/7/students/101/progress"]')).not.toBeNull();
    expect(root.textContent).not.toContain('142 hoạt động');
  });

  it('rejects an invalid course route ID without issuing any API request', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/mentor/courses/not-an-id', ME03Page);
    harness.fixture.detectChanges();

    expect(page.invalidId()).toBe(true);
    expect(harness.routeNativeElement?.querySelector('[role="alert"]')?.textContent).toContain(
      'Course ID trên đường dẫn không phải số nguyên dương int64.',
    );
    http.expectNone('/api/v1/mentor/courses');
    http.expectNone('/api/v1/mentor/courses/not-an-id/content');
    http.expectNone('/api/v1/mentor/courses/not-an-id/progress');
  });

  it('fails closed when one course endpoint denies access', async () => {
    signInAsMentor();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/mentor/courses/7', ME03Page);

    const coursesRequest = expectGet('/api/v1/mentor/courses');
    const contentRequest = expectGet('/api/v1/mentor/courses/7/content');
    const progressRequest = expectGet('/api/v1/mentor/courses/7/progress');
    contentRequest.flush(
      {
        success: false,
        businessCode: 'DESIGN_FORBIDDEN',
        message: 'Course access denied.',
        data: null,
        meta: {},
        traceId: 'me03-forbidden',
      },
      { status: 403, statusText: 'Forbidden' },
    );
    progressRequest.flush(successEnvelope(progressPage([progressRow()])));
    coursesRequest.flush(successEnvelope(coursePage([course()], 1, 20, 1)));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(page.accessError()).toBe('Course access denied.');
    expect(page.courseTitle()).toBe('Workspace khóa học');
    expect(page.content()).toEqual([]);
    expect(page.progress()).toEqual([]);
    expect(harness.routeNativeElement?.textContent).not.toContain('Student One');
    expect(harness.routeNativeElement?.textContent).not.toContain('Unit A');
    expect(harness.routeNativeElement?.querySelector('a[href="/mentor/courses/7/lectures/new"]')).toBeNull();
  });

  it('reports invalid #49 code and #65 projection with validation errors', async () => {
    signInAsMentor();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/mentor/courses/7', ME03Page);

    expectGet('/api/v1/mentor/courses').flush(successEnvelope(coursePage([course()], 1, 20, 1)));
    expectGet('/api/v1/mentor/courses/7/content').flush(
      successEnvelope([content(81, null, 'Untrusted content')], 'DESIGN_RESOURCE_UPDATED'),
    );
    expectGet('/api/v1/mentor/courses/7/progress').flush(
      successEnvelope(progressPage([{ ...progressRow(), progress_percent: 101 }])),
    );
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(page.content()).toEqual([]);
    expect(page.progress()).toEqual([]);
    expect(page.contentError()).toBe('Study Server trả về cây nội dung không hợp lệ.');
    expect(page.progressError()).toBe('Study Server trả về tiến độ không hợp lệ.');
    expect(harness.routeNativeElement?.textContent).not.toContain('Untrusted content');
    expect(harness.routeNativeElement?.textContent).not.toContain('Student One');
  });

  it('preserves API messages for actual unsuccessful #49 and #65 envelopes', async () => {
    signInAsMentor();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/mentor/courses/7', ME03Page);

    expectGet('/api/v1/mentor/courses').flush(successEnvelope(coursePage([course()], 1, 20, 1)));
    expectGet('/api/v1/mentor/courses/7/content').flush(failureEnvelope('Content read failed.'));
    expectGet('/api/v1/mentor/courses/7/progress').flush(failureEnvelope('Progress read failed.'));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(page.contentError()).toBe('Content read failed.');
    expect(page.progressError()).toBe('Progress read failed.');
    expect(page.content()).toEqual([]);
    expect(page.progress()).toEqual([]);
  });

  function expectGet(url: string) {
    const request = http.expectOne((candidate) => candidate.url === url);
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer mentor-access-token');
    expect(request.request.body).toBeNull();
    expect(request.request.params.keys()).toEqual([]);
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
    traceId: 'me03-test',
  };
}

function failureEnvelope(message: string): ApiEnvelope<null> {
  return {
    success: false,
    businessCode: 'DESIGN_INTERNAL_ERROR',
    message,
    data: null,
    meta: {},
    traceId: 'me03-error',
  };
}

function coursePage(
  items: MentorCourse[],
  page: number,
  size: number,
  total: number,
): MentorPage<MentorCourse> {
  const totalPages = total === 0 ? 0 : Math.ceil(total / size);
  return { items, pagination: { page, size, total, total_pages: totalPages } };
}

function course(): MentorCourse {
  return {
    id: 7,
    title: 'English Basics',
    description: 'Course description.',
    thumbnail_url: null,
    price: '10.00',
    status: 'PUBLISHED',
    mentor: { id: 5, full_name: 'Mentor One', avatar_url: null },
  };
}

function content(
  id: number,
  parentId: number | null,
  title: string,
): MentorContent {
  return {
    id,
    course_id: 7,
    content_type: 'LESSON',
    title,
    payload: {},
    status: 'PUBLISHED',
    parent_id: parentId,
    order: id,
  };
}

function progressRow(): MentorCourseProgressRow {
  return {
    student: { id: 101, full_name: 'Student One', avatar_url: null },
    completed_lessons: 2,
    total_lessons: 3,
    progress_percent: 66,
  };
}

function progressPage(
  items: MentorCourseProgressRow[],
): MentorPage<MentorCourseProgressRow> {
  return {
    items,
    pagination: {
      page: 1,
      size: items.length,
      total: items.length,
      total_pages: items.length > 0 ? 1 : 0,
    },
  };
}
