import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type {
  GuestCatalogPagination,
  GuestPublicCourse,
  GuestPublicCoursePage,
} from '../../shared/models/guest-course.models';
import { SH06Page } from '../../../shared/SH06/pages/sh06-page';
import { GS03Page } from './gs03-page';

describe('GS03Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GS03Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([
          { path: 'courses/:courseId', component: GS03Page },
          { path: 'not-found', component: SH06Page },
        ]),
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('loads the overview first and fetches curriculum only after selecting its tab', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/courses/42', GS03Page);

    const request = http.expectOne('/api/v1/courses/42');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.has('Authorization')).toBe(false);
    request.flush(successEnvelope(coursePage([course(42)])));
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Kiến thức nền tảng');
    expect(root.textContent).toContain('Nguyen Van Mentor');
    expect(root.textContent).not.toContain('59.90');
    expect(root.querySelector('[role="tab"][aria-selected="true"]')?.textContent).toContain(
      'Tổng quan',
    );
    expect(root.querySelectorAll('[role="tab"][disabled]')).toHaveLength(0);
    http.expectNone('/api/v1/courses/42/curriculum');
    http.expectNone('/api/v1/courses/42/reviews');
    http.expectNone('/api/v1/courses/42/resources');

    root.querySelector<HTMLButtonElement>('#gs03-tab-curriculum')?.click();
    harness.fixture.detectChanges();
    await harness.fixture.whenStable();

    expect(TestBed.inject(Router).url).toBe('/courses/42?tab=curriculum');
    const curriculumRequest = http.expectOne('/api/v1/courses/42/curriculum');
    expect(curriculumRequest.request.method).toBe('GET');
    expect(curriculumRequest.request.headers.has('Authorization')).toBe(false);
    curriculumRequest.flush(successEnvelope(curriculumPage([])));
    harness.fixture.detectChanges();

    expect((harness.routeNativeElement as HTMLElement).textContent).toContain(
      'Chưa có nội dung đề cương để hiển thị.',
    );
  });

  it('supports direct curriculum entry and preserves a large route id as text', async () => {
    const courseId = '9223372036854775807';
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl(`/courses/${courseId}?tab=curriculum`, GS03Page);

    const detailRequest = http.expectOne(`/api/v1/courses/${courseId}`);
    expect(detailRequest.request.headers.has('Authorization')).toBe(false);
    http.expectNone(`/api/v1/courses/${courseId}/curriculum`);
    detailRequest.flush(successEnvelope(coursePage([course(42)])));
    harness.fixture.detectChanges();

    const curriculumRequest = http.expectOne(`/api/v1/courses/${courseId}/curriculum`);
    expect(curriculumRequest.request.headers.has('Authorization')).toBe(false);
    curriculumRequest.flush(
      successEnvelope(
        curriculumPage([
          {
            id: 9,
            course_id: 42,
            title: 'Bài học thứ hai',
            content: 'Nội dung riêng không được hiển thị.',
            video_url: 'https://example.test/private-video.mp4',
            order: 2,
            status: 'PUBLISHED',
          },
          {
            id: 8,
            course_id: 42,
            title: 'Bài học đầu tiên',
            content: null,
            video_url: null,
            order: 1,
            status: 'PUBLISHED',
          },
        ]),
      ),
    );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const curriculum = root.querySelector('#gs03-curriculum');
    expect(root.textContent).toContain('Bài học đầu tiên');
    expect(root.textContent).toContain('Bài học thứ hai');
    expect(
      [...(curriculum?.querySelectorAll('.lesson-title') ?? [])].map((node) =>
        node.textContent?.trim(),
      ),
    ).toEqual(['Bài học đầu tiên', 'Bài học thứ hai']);
    expect(root.textContent).not.toContain('Nội dung riêng không được hiển thị');
    expect(root.textContent).not.toContain('private-video.mp4');
    expect(curriculum?.querySelectorAll('.lesson-row a, .lesson-row button')).toHaveLength(0);
    expect(root.querySelector('[role="tab"][aria-selected="true"]')?.textContent).toContain(
      'Đề cương',
    );
  });

  it('loads public reviews only after the published course check and preserves the route id', async () => {
    const courseId = '9223372036854775807';
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl(`/courses/${courseId}?tab=reviews`, GS03Page);

    const detailRequest = http.expectOne(`/api/v1/courses/${courseId}`);
    expect(detailRequest.request.headers.has('Authorization')).toBe(false);
    http.expectNone((request) => request.url.includes('/reviews'));
    detailRequest.flush(successEnvelope(coursePage([course(42)])));
    harness.fixture.detectChanges();

    const reviewsRequest = http.expectOne(`/api/v1/courses/${courseId}/reviews?page=1`);
    expect(reviewsRequest.request.method).toBe('GET');
    expect(reviewsRequest.request.headers.has('Authorization')).toBe(false);
    reviewsRequest.flush(
      successEnvelope(
        reviewsPage(
          [
            {
              id: 31,
              course_id: 42,
              title: null,
              content: 'Nội dung thảo luận được hiển thị.',
              author: { id: 3, full_name: 'Le Minh', avatar_url: null },
              status: 'ACTIVE',
              created_at: '2026-11-17T00:00:00Z',
              comments: [],
            },
          ],
          1,
          1,
        ),
      ),
    );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Nội dung thảo luận được hiển thị.');
    expect(root.textContent).toContain('Le Minh');
    expect(root.querySelector('[role="tab"][aria-selected="true"]')?.textContent).toContain(
      'Đánh giá',
    );
  });

  it('supports End-key navigation to the public resources tab', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/courses/42', GS03Page);
    http.expectOne('/api/v1/courses/42').flush(successEnvelope(coursePage([course(42)])));
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    root.querySelector<HTMLButtonElement>('#gs03-tab-overview')?.dispatchEvent(
      new KeyboardEvent('keydown', { key: 'End', bubbles: true }),
    );
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(TestBed.inject(Router).url).toBe('/courses/42?tab=resources');
    expect(root.querySelector('#gs03-tab-resources')?.getAttribute('aria-selected')).toBe('true');
    http
      .expectOne('/api/v1/courses/42/resources')
      .flush(successEnvelope([{ id: 4, name: 'Tài liệu công khai', type: 'DOCUMENT', url: 'https://cdn.example.test/4.pdf', visibility: 'PUBLIC', lesson_id: 12 }]));
    harness.fixture.detectChanges();
    expect(root.textContent).toContain('Tài liệu công khai');
    http.expectNone((request) => request.url.startsWith('/api/v1/resources/'));
  });

  it('opens the public resources tab only after the published-course check', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/courses/42?tab=resources', GS03Page);

    const detailRequest = http.expectOne('/api/v1/courses/42');
    expect(detailRequest.request.headers.has('Authorization')).toBe(false);
    http.expectNone('/api/v1/courses/42/resources');
    http.expectNone((request) => request.url.startsWith('/api/v1/resources/'));
    detailRequest.flush(successEnvelope(coursePage([course(42)])));
    harness.fixture.detectChanges();
    const resourcesRequest = http.expectOne('/api/v1/courses/42/resources');
    expect(resourcesRequest.request.method).toBe('GET');
    expect(resourcesRequest.request.headers.has('Authorization')).toBe(false);
    resourcesRequest.flush(successEnvelope([]));
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('#gs03-tab-resources')?.getAttribute('aria-selected')).toBe('true');
    expect(root.textContent).toContain('Khóa học chưa có tài liệu công khai.');
    expect(TestBed.inject(Router).url).toBe('/courses/42?tab=resources');
    http.expectNone((request) => request.url.startsWith('/api/v1/resources/'));
  });

  it('shows not-found when the curriculum API returns 404', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/courses/42?tab=curriculum', GS03Page);
    http.expectOne('/api/v1/courses/42').flush(successEnvelope(coursePage([course(42)])));

    http
      .expectOne('/api/v1/courses/42/curriculum')
      .flush({ message: 'private backend detail' }, { status: 404, statusText: 'Not Found' });
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Không tìm thấy đề cương khóa học này.');
    expect(root.textContent).not.toContain('private backend detail');
  });

  it('shows a safe service error when the curriculum API fails', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/courses/42?tab=curriculum', GS03Page);
    http.expectOne('/api/v1/courses/42').flush(successEnvelope(coursePage([course(42)])));

    http
      .expectOne('/api/v1/courses/42/curriculum')
      .flush(
        { message: 'internal curriculum detail' },
        { status: 500, statusText: 'Server Error' },
      );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Chưa thể tải đề cương. Vui lòng thử lại sau.');
    expect(root.textContent).not.toContain('internal curriculum detail');
    root.querySelector<HTMLButtonElement>('#gs03-curriculum .retry-button')?.click();
    http
      .expectOne('/api/v1/courses/42/curriculum')
      .flush(
        successEnvelope(
          curriculumPage([
            {
              id: 13,
              course_id: 42,
              title: 'Đề cương đã tải lại',
              content: null,
              video_url: null,
              order: 1,
              status: 'PUBLISHED',
            },
          ]),
        ),
      );
    harness.fixture.detectChanges();
    expect(root.textContent).toContain('Đề cương đã tải lại');
  });

  it('routes a missing or non-public course response to SH-06 without exposing the course id or API detail', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/courses/732119', GS03Page);

    http
      .expectOne('/api/v1/courses/732119')
      .flush({ message: 'private course detail' }, { status: 404, statusText: 'Not Found' });
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(TestBed.inject(Router).url).toBe('/not-found');
    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Không tìm thấy trang hoặc tài nguyên yêu cầu');
    expect(root.textContent).not.toContain('private course detail');
    expect(root.textContent).not.toContain('732119');
    http.expectNone('/api/v1/courses/732119/curriculum');
  });

  it('shows a safe service error for a failed detail request', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/courses/42', GS03Page);

    http
      .expectOne('/api/v1/courses/42')
      .flush({ message: 'internal detail' }, { status: 500, statusText: 'Server Error' });
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Chưa thể tải thông tin khóa học');
    expect(root.textContent).not.toContain('internal detail');
    root.querySelector<HTMLButtonElement>('.primary-button')?.click();
    http
      .expectOne('/api/v1/courses/42')
      .flush(successEnvelope(coursePage([course(42)])));
    harness.fixture.detectChanges();
    expect(root.textContent).toContain('Kiến thức nền tảng');
  });

  it('falls back to placeholders when course cover and mentor avatar fail to load', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/courses/42', GS03Page);

    http
      .expectOne('/api/v1/courses/42')
      .flush(
        successEnvelope(
          coursePage([
            {
              ...course(42),
              thumbnail_url: 'https://cdn.example.com/course-broken.png',
              mentor: {
                id: 7,
                full_name: 'Nguyen Van Mentor',
                avatar_url: 'https://cdn.example.com/avatar-broken.png',
              },
            },
          ]),
        ),
      );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const coverImg = root.querySelector<HTMLImageElement>('img.course-image');
    const avatarImg = root.querySelector<HTMLImageElement>('img.mentor-avatar');
    expect(coverImg).not.toBeNull();
    expect(avatarImg).not.toBeNull();

    coverImg!.dispatchEvent(new Event('error'));
    avatarImg!.dispatchEvent(new Event('error'));
    harness.fixture.detectChanges();

    expect(root.querySelector('img.course-image')).toBeNull();
    expect(root.querySelector('.course-image--empty')).not.toBeNull();
    expect(root.querySelector('img.mentor-avatar')).toBeNull();
    expect(root.querySelector('.mentor-avatar--empty')).not.toBeNull();
  });
});

function course(id: number): GuestPublicCourse {
  return {
    id,
    title: 'Kiến thức nền tảng',
    description: 'Mô tả khóa học.',
    thumbnail_url: null,
    price: '59.90',
    status: 'PUBLISHED',
    mentor: { id: 7, full_name: 'Nguyen Van Mentor', avatar_url: null },
  };
}

function coursePage(items: GuestPublicCourse[]): GuestPublicCoursePage {
  return {
    items,
    pagination: { page: 1, size: 1, total: 1, total_pages: 1 } satisfies GuestCatalogPagination,
  };
}

function curriculumPage(items: GuestCurriculumFixture[]): GuestCurriculumPageFixture {
  return {
    items,
    pagination: {
      page: 1,
      size: items.length,
      total: items.length,
      total_pages: items.length ? 1 : 0,
    },
  };
}

function reviewsPage(
  items: GuestReviewFixture[],
  page: number,
  totalPages: number,
): GuestReviewsPageFixture {
  return {
    items,
    pagination: { page, size: 20, total: items.length, total_pages: totalPages },
  };
}

interface GuestCurriculumFixture {
  id: number;
  course_id: number;
  title: string;
  content: string | null;
  video_url: string | null;
  order: number;
  status: string;
}

interface GuestCurriculumPageFixture {
  items: GuestCurriculumFixture[];
  pagination: { page: number; size: number; total: number; total_pages: number };
}

interface GuestReviewFixture {
  id: number;
  course_id: number;
  title: string | null;
  content: string;
  author: { id: number; full_name: string; avatar_url: string | null };
  status: string;
  created_at: string;
  comments: {
    id: number;
    discussion_id: number;
    content: string;
    author: { id: number; full_name: string; avatar_url: string | null };
    created_at: string;
  }[];
}

interface GuestReviewsPageFixture {
  items: GuestReviewFixture[];
  pagination: { page: number; size: number; total: number; total_pages: number };
}

function successEnvelope<T>(data: T): ApiEnvelope<T> {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'ok',
    data,
    meta: {},
    traceId: 'test-trace',
  };
}
