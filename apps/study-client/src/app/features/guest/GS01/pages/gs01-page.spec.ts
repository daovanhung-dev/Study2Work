import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { Location } from '@angular/common';
import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type {
  GuestCategory,
  GuestCategoryPage,
  GuestCatalogPagination,
  GuestPublicCourse,
  GuestPublicCoursePage,
} from '../../shared/models/guest-course.models';
import { GS01Page } from './gs01-page';
import { GS03Page } from '../../GS03/pages/gs03-page';

@Component({ standalone: true, template: '<p>Search route</p>' })
class SearchRouteStub {}

describe('GS01Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GS01Page, GS03Page, SearchRouteStub],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([
          {
            path: 'courses',
            children: [
              { path: 'search', component: SearchRouteStub },
              { path: ':courseId', component: GS03Page },
              { path: '', component: GS01Page },
            ],
          },
        ]),
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('loads categories before the public course page without sending a category filter', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/courses', GS01Page);

    const categories = http.expectOne('/api/v1/categories');
    expect(categories.request.method).toBe('GET');
    expect(categories.request.headers.has('Authorization')).toBe(false);
    http.expectNone('/api/v1/courses');

    categories.flush(successEnvelope(categoryPage([category(1, 'Lập trình')])));
    const courses = http.expectOne(
      (request) =>
        request.url === '/api/v1/courses' &&
        request.params.get('page') === '1' &&
        request.params.get('size') === '20',
    );
    expect(courses.request.method).toBe('GET');
    expect(courses.request.params.keys().sort()).toEqual(['page', 'size']);
    expect(courses.request.headers.has('Authorization')).toBe(false);
    courses.flush(
      successEnvelope(
        coursePage({
          items: [course(101, 'React cơ bản')],
          pagination: pagination({ page: 1, size: 20, total: 1, total_pages: 1 }),
        }),
      ),
    );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(page.catalogState()).toMatchObject({ status: 'ready' });
    expect(root.textContent).toContain('Lập trình');
    expect(root.textContent).toContain('React cơ bản');
    expect(root.textContent).toContain('Nguyen Van Mentor');
    expect(root.textContent).toContain('1 khóa học');
    expect(root.textContent).not.toContain('59.90');
    expect(root.querySelector<HTMLAnchorElement>('.course-link')?.getAttribute('href')).toBe(
      '/courses/101',
    );
  });

  it('continues to the course request when category metadata fails', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/courses', GS01Page);

    http
      .expectOne('/api/v1/categories')
      .flush({ message: 'temporary failure' }, { status: 500, statusText: 'Server error' });
    const courses = http.expectOne(
      (request) => request.url === '/api/v1/courses' && request.params.get('page') === '1',
    );
    expect(courses.request.params.has('category')).toBe(false);
    courses.flush(
      successEnvelope(
        coursePage({
          items: [],
          pagination: pagination({ page: 1, size: 20, total: 0, total_pages: 0 }),
        }),
      ),
    );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Danh mục chưa thể tải.');
    expect(root.textContent).toContain('Chưa có khóa học nào');
  });

  it('keeps course rows and retries when the count and list snapshots disagree', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/courses', GS01Page);
    http.expectOne('/api/v1/categories').flush(successEnvelope(categoryPage([])));
    http
      .expectOne((request) => request.url === '/api/v1/courses')
      .flush(
        successEnvelope(
          coursePage({
            items: [course(101, 'React cơ bản')],
            pagination: pagination({ page: 1, size: 20, total: 2, total_pages: 1 }),
          }),
        ),
      );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('React cơ bản');
    expect(root.textContent).toContain('Số khóa học và danh sách trang chưa đồng nhất');
    expect(root.querySelector('.results-summary, .pagination')).toBeNull();
    expect(page.catalogSnapshotMismatch()).toBe(true);
    root.querySelector<HTMLButtonElement>('.primary-button')?.click();

    http
      .expectOne((request) => request.url === '/api/v1/courses' && request.params.get('page') === '1')
      .flush(
        successEnvelope(
          coursePage({
            items: [course(101, 'React cơ bản'), course(102, 'React nâng cao')],
            pagination: pagination({ page: 1, size: 20, total: 2, total_pages: 1 }),
          }),
        ),
      );
    harness.fixture.detectChanges();

    expect(page.catalogSnapshotMismatch()).toBe(false);
    expect(root.textContent).toContain('2 khóa học');
  });

  it('resets to page one when sorting and preserves the sort when paging', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/courses', GS01Page);

    http.expectOne('/api/v1/categories').flush(successEnvelope(categoryPage([])));
    http
      .expectOne((request) => request.params.get('page') === '1')
      .flush(
        successEnvelope(
          coursePage({
            items: Array.from({ length: 20 }, (_, index) =>
              course(100 + index, index === 0 ? 'React cơ bản' : `Khóa học ${index + 1}`),
            ),
            pagination: pagination({ page: 1, size: 20, total: 21, total_pages: 2 }),
          }),
        ),
      );
    harness.fixture.detectChanges();

    const sort = (harness.routeNativeElement as HTMLElement).querySelector<HTMLSelectElement>(
      '.sort-control select',
    );
    expect(sort).not.toBeNull();
    sort!.value = 'name:asc';
    sort!.dispatchEvent(new Event('change', { bubbles: true }));

    const sortedPage = http.expectOne(
      (request) =>
        request.url === '/api/v1/courses' &&
        request.params.get('page') === '1' &&
        request.params.get('size') === '20' &&
        request.params.get('sort') === 'name:asc',
    );
    sortedPage.flush(
      successEnvelope(
        coursePage({
          items: Array.from({ length: 20 }, (_, index) =>
            course(100 + index, index === 0 ? 'React cơ bản' : `Khóa học ${index + 1}`),
          ),
          pagination: pagination({ page: 1, size: 20, total: 21, total_pages: 2 }),
        }),
      ),
    );
    harness.fixture.detectChanges();

    expect(
      (harness.routeNativeElement as HTMLElement).querySelector<HTMLSelectElement>(
        '.sort-control select',
      )?.value,
    ).toBe('name:asc');

    (harness.routeNativeElement as HTMLElement)
      .querySelector<HTMLButtonElement>('.pagination button:last-child')!
      .click();
    const secondPage = http.expectOne(
      (request) => request.params.get('page') === '2' && request.params.get('sort') === 'name:asc',
    );
    secondPage.flush(
      successEnvelope(
        coursePage({
          items: [course(102, 'TypeScript nâng cao')],
          pagination: pagination({ page: 2, size: 20, total: 21, total_pages: 2 }),
        }),
      ),
    );
    harness.fixture.detectChanges();

    expect(page.catalogState()).toMatchObject({
      status: 'ready',
      result: { pagination: { page: 2 } },
    });
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain(
      'TypeScript nâng cao',
    );
  });

  it('sends a nonblank hero search to the existing GS02 route', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/courses', GS01Page);
    http.expectOne('/api/v1/categories').flush(successEnvelope(categoryPage([])));
    http
      .expectOne((request) => request.url === '/api/v1/courses')
      .flush(
        successEnvelope(
          coursePage({
            items: [],
            pagination: pagination({ page: 1, size: 20, total: 0, total_pages: 0 }),
          }),
        ),
      );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const input = root.querySelector<HTMLInputElement>('#gs01-course-search')!;
    input.value = '  React  ';
    input.dispatchEvent(new Event('input', { bubbles: true }));
    root
      .querySelector('form.hero-search')!
      .dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    await harness.fixture.whenStable();

    const path = new URL(TestBed.inject(Location).path(), 'http://localhost');
    expect(path.pathname).toBe('/courses/search');
    expect(path.searchParams.get('q')).toBe('React');
  });

  it('falls back to placeholder cover when course thumbnail fails to load', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/courses', GS01Page);
    http.expectOne('/api/v1/categories').flush(successEnvelope(categoryPage([])));
    http
      .expectOne((request) => request.url === '/api/v1/courses')
      .flush(
        successEnvelope(
          coursePage({
            items: [{ ...course(101, 'React cơ bản'), thumbnail_url: 'https://cdn.example.com/broken.png' }],
            pagination: pagination({ page: 1, size: 20, total: 1, total_pages: 1 }),
          }),
        ),
      );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const img = root.querySelector<HTMLImageElement>('img.course-cover');
    expect(img).not.toBeNull();
    img!.dispatchEvent(new Event('error'));
    harness.fixture.detectChanges();

    expect(root.querySelector('img.course-cover')).toBeNull();
    expect(root.querySelector('.course-cover--empty')).not.toBeNull();
  });
});

function category(id: number, name: string): GuestCategory {
  return { id, name, slug: `category-${id}`, description: null };
}

function course(id: number, title: string): GuestPublicCourse {
  return {
    id,
    title,
    description: 'Nội dung khóa học',
    thumbnail_url: null,
    price: '59.90',
    status: 'PUBLISHED',
    mentor: { id: 7, full_name: 'Nguyen Van Mentor', avatar_url: null },
  };
}

function categoryPage(items: GuestCategory[]): GuestCategoryPage {
  return {
    items,
    pagination: pagination({ page: 1, size: items.length, total: items.length, total_pages: 1 }),
  };
}

function coursePage(data: GuestPublicCoursePage): GuestPublicCoursePage {
  return data;
}

function pagination(data: GuestCatalogPagination): GuestCatalogPagination {
  return data;
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
