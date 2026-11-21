import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type {
  SH01Category,
  SH01CategoryPage,
  SH01PublicCourse,
  SH01PublicCoursePage,
} from '../models/sh01-catalog.models';
import { SH01Page } from './sh01-page';

describe('SH01Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SH01Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([{ path: '', component: SH01Page }]),
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('requests #05 and #06 independently and renders only published response data', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/', SH01Page);

    const categories = http.expectOne('/api/v1/categories');
    const courses = http.expectOne((request) =>
      request.url === '/api/v1/courses'
      && request.params.get('page') === '1'
      && request.params.get('size') === '6',
    );
    expect(categories.request.method).toBe('GET');
    expect(categories.request.headers.has('Authorization')).toBe(false);
    expect(courses.request.method).toBe('GET');
    expect(courses.request.params.keys().sort()).toEqual(['page', 'size']);
    expect(courses.request.headers.has('Authorization')).toBe(false);
    expect(page.categoryState()).toEqual({ status: 'loading' });
    expect(page.courseState()).toEqual({ status: 'loading' });
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain('Đang tải danh mục…');
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain('Đang tải khóa học…');
    expect((harness.routeNativeElement as HTMLElement).querySelectorAll('.course-skeleton'))
      .toHaveLength(6);

    categories.flush(successEnvelope(categoryPage([category(1, 'Lập trình')])));
    courses.flush(successEnvelope(coursePage([
      course(101, 'Khóa học công khai', 'PUBLISHED', 'https://cdn.example.test/mentor.png'),
      course(102, 'Khóa học không công khai', 'DRAFT'),
      course(103, 'Khóa học có ảnh bìa', 'PUBLISHED', null, 'https://cdn.example.test/course.png'),
    ])));
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(page.categoryState()).toMatchObject({ status: 'ready' });
    expect(page.courseState()).toMatchObject({ status: 'ready' });
    expect(root.textContent).toContain('Lập trình');
    expect(root.textContent).toContain('Khóa học công khai');
    expect(root.textContent).toContain('Nguyen Van Mentor');
    expect(root.textContent).not.toContain('Khóa học không công khai');
    expect(root.textContent).not.toContain('59.90');
    expect(root.textContent).not.toContain('Dữ liệu minh họa');
    expect(root.querySelector<HTMLImageElement>('img.mentor-avatar')?.getAttribute('src'))
      .toBe('https://cdn.example.test/mentor.png');
    const thumbnail = root.querySelector<HTMLImageElement>('.course-card img.course-thumbnail');
    expect(thumbnail?.getAttribute('src')).toBe('https://cdn.example.test/course.png');
    expect(root.querySelectorAll('.category-list a, .category-list button')).toHaveLength(0);
    expect(root.querySelectorAll('.course-card a, .course-card button')).toHaveLength(0);
    expect(root.querySelector('.skip-link')?.getAttribute('href')).toBe('#sh01-main');
    expect(root.querySelector('main#sh01-main')).not.toBeNull();
    expect(root.querySelector<HTMLAnchorElement>('.hero-links .primary-button')?.getAttribute('href'))
      .toBe('/courses');
    expect(root.querySelector<HTMLAnchorElement>('.hero-links .secondary-button')?.getAttribute('href'))
      .toBe('/register');

    root.querySelector<HTMLImageElement>('img.mentor-avatar')?.dispatchEvent(new Event('error'));
    harness.fixture.detectChanges();
    expect(root.querySelector('img.mentor-avatar')).toBeNull();
    expect(root.querySelector('.mentor-avatar--empty')).not.toBeNull();
    thumbnail?.dispatchEvent(new Event('error'));
    harness.fixture.detectChanges();
    expect(root.querySelector('.course-card img.course-thumbnail')).toBeNull();
    expect(root.querySelector('.course-card .course-thumbnail--empty')).not.toBeNull();
  });

  it('keeps blank search on SH-01 and hands trimmed Unicode query to GS-02', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/', SH01Page);
    http.expectOne('/api/v1/categories').flush(successEnvelope(categoryPage([])));
    http.expectOne((request) => request.url === '/api/v1/courses')
      .flush(successEnvelope(coursePage([])));

    const navigate = vi.spyOn(TestBed.inject(Router), 'navigate').mockResolvedValue(true);
    page.searchQuery.set('   ');
    page.submitSearch();
    expect(navigate).not.toHaveBeenCalled();

    page.searchQuery.set('  C++ & Ứng dụng  ');
    page.submitSearch();
    expect(navigate).toHaveBeenCalledOnce();
    expect(navigate).toHaveBeenCalledWith(['/courses/search'], {
      queryParams: { q: 'C++ & Ứng dụng' },
    });
  });

  it('keeps the landing route when a public catalog request returns unauthorized', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/', SH01Page);

    http.expectOne('/api/v1/categories')
      .flush({}, { status: 401, statusText: 'Unauthorized' });
    http.expectOne((request) => request.url === '/api/v1/courses')
      .flush(successEnvelope(coursePage([course(101, 'Khóa học công khai')])));
    harness.fixture.detectChanges();

    expect(page.categoryState()).toEqual({ status: 'error' });
    expect(page.courseState()).toMatchObject({ status: 'ready' });
    expect(TestBed.inject(Router).url).toBe('/');
  });

  it('keeps the course region available and retries only categories after a category error', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/', SH01Page);

    http.expectOne('/api/v1/categories')
      .flush({}, { status: 500, statusText: 'Server error' });
    http.expectOne((request) => request.url === '/api/v1/courses')
      .flush(successEnvelope(coursePage([course(101, 'Khóa học công khai')])));
    harness.fixture.detectChanges();

    expect(page.categoryState()).toMatchObject({ status: 'error' });
    expect(page.courseState()).toMatchObject({ status: 'ready' });
    (harness.routeNativeElement as HTMLElement)
      .querySelector<HTMLButtonElement>('.category-section .text-button')!
      .click();

    const retry = http.expectOne('/api/v1/categories');
    expect(retry.request.method).toBe('GET');
    http.expectNone((request) => request.url === '/api/v1/courses');
    retry.flush(successEnvelope(categoryPage([category(2, 'Thiết kế')])));
    harness.fixture.detectChanges();

    expect(page.categoryState()).toMatchObject({ status: 'ready' });
    expect(page.courseState()).toMatchObject({ status: 'ready' });
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain('Thiết kế');
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain('Khóa học công khai');
  });

  it('keeps categories available and retries only courses after a course error', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/', SH01Page);

    http.expectOne('/api/v1/categories')
      .flush(successEnvelope(categoryPage([category(1, 'Lập trình')])));
    http.expectOne((request) => request.url === '/api/v1/courses')
      .flush({}, { status: 500, statusText: 'Server error' });
    harness.fixture.detectChanges();

    expect(page.categoryState()).toMatchObject({ status: 'ready' });
    expect(page.courseState()).toMatchObject({ status: 'error' });
    (harness.routeNativeElement as HTMLElement)
      .querySelector<HTMLButtonElement>('.course-heading + .region-status .text-button')!
      .click();

    const retry = http.expectOne((request) => request.url === '/api/v1/courses');
    expect(retry.request.params.get('page')).toBe('1');
    expect(retry.request.params.get('size')).toBe('6');
    http.expectNone('/api/v1/categories');
    retry.flush(successEnvelope(coursePage([course(101, 'Khóa học công khai')])));
    harness.fixture.detectChanges();

    expect(page.categoryState()).toMatchObject({ status: 'ready' });
    expect(page.courseState()).toMatchObject({ status: 'ready' });
  });

  it('treats malformed success projections as errors instead of empty results', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/', SH01Page);

    http.expectOne('/api/v1/categories').flush(successEnvelope({
      items: [{ id: 'invalid', name: 'Không hợp lệ', slug: 'invalid' }],
      pagination: { page: 1, size: 1, total: 1, total_pages: 1 },
    }));
    http.expectOne((request) => request.url === '/api/v1/courses')
      .flush(successEnvelope({
        items: [{ id: 101, title: 'Thiếu mentor' }],
        pagination: { page: 1, size: 6, total: 1, total_pages: 1 },
      }));
    harness.fixture.detectChanges();

    expect(page.categoryState()).toEqual({ status: 'error' });
    expect(page.courseState()).toEqual({ status: 'error' });
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain('Thử lại');
    expect((harness.routeNativeElement as HTMLElement).textContent)
      .not.toContain('Không hợp lệ');
    expect((harness.routeNativeElement as HTMLElement).textContent)
      .not.toContain('Thiếu mentor');
  });

  it('shows independent empty states without creating sample items', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/', SH01Page);

    http.expectOne('/api/v1/categories')
      .flush(successEnvelope(categoryPage([])));
    http.expectOne((request) => request.url === '/api/v1/courses')
      .flush(successEnvelope(coursePage([])));
    harness.fixture.detectChanges();

    expect(page.categoryState()).toEqual({ status: 'empty' });
    expect(page.courseState()).toEqual({ status: 'empty' });
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain('Hiện chưa có danh mục.');
    expect((harness.routeNativeElement as HTMLElement).textContent)
      .toContain('Hiện chưa có khóa học đã xuất bản.');
    expect((harness.routeNativeElement as HTMLElement).textContent)
      .not.toContain('Lập trình Web Frontend với React');
  });
});

function category(id: number, name: string): SH01Category {
  return { id, name, slug: `category-${id}`, description: null };
}

function course(
  id: number,
  title: string,
  status = 'PUBLISHED',
  avatarUrl: string | null = null,
  thumbnailUrl: string | null = null,
): SH01PublicCourse {
  return {
    id,
    title,
    description: 'Mô tả do API trả về',
    thumbnail_url: thumbnailUrl,
    price: '59.90',
    status,
    mentor: { id: 7, full_name: 'Nguyen Van Mentor', avatar_url: avatarUrl },
  };
}

function categoryPage(items: SH01Category[]): SH01CategoryPage {
  return {
    items,
    pagination: { page: 1, size: items.length, total: items.length, total_pages: 1 },
  };
}

function coursePage(items: SH01PublicCourse[]): SH01PublicCoursePage {
  return {
    items,
    pagination: { page: 1, size: 6, total: items.length, total_pages: items.length ? 1 : 0 },
  };
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
