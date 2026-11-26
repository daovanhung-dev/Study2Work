import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { Location } from '@angular/common';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type {
  GS02Course,
  GS02CourseSearchPage,
  GS02Pagination,
} from '../models/gs02-search.models';
import { GS02Page } from './gs02-page';

describe('GS02Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GS02Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([{ path: 'courses/search', component: GS02Page }]),
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('shows a prompt and makes no request when the URL has no nonblank q', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/courses/search?q=%20%20', GS02Page);

    expect((harness.routeNativeElement as HTMLElement).textContent).toContain(
      'Nhập từ khóa để xem kết quả',
    );
    http.expectNone('/api/v1/courses/search');
  });

  it('normalizes URL q and renders only fields returned by API #07', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/courses/search?q=%20%20REACT%20', GS02Page);

    const request = http.expectOne(
      (candidate) =>
        candidate.url === '/api/v1/courses/search' &&
        candidate.params.get('q') === 'react' &&
        candidate.params.get('page') === '1',
    );
    expect(request.request.method).toBe('GET');
    expect(request.request.params.keys().sort()).toEqual(['page', 'q']);
    expect(request.request.headers.has('Authorization')).toBe(false);
    request.flush(
      successEnvelope(
        coursePage({
          items: [course(101, 'React cơ bản')],
          pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
        }),
      ),
    );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('study-guest-site-layout header.site-header')).not.toBeNull();
    expect(root.querySelector('study-guest-site-layout footer.site-footer')).not.toBeNull();
    expect(root.querySelector('[data-screen-id="GS02"]')).not.toBeNull();
    expect(root.textContent).toContain('React cơ bản');
    expect(root.textContent).toContain('Nguyen Van Mentor');
    expect(root.textContent).toContain('Fundamentals of React');
    expect(root.textContent).not.toContain('49.90');
    expect(root.querySelector<HTMLAnchorElement>('.course-card__link')?.getAttribute('href')).toBe(
      '/courses/101',
    );
    expect(root.querySelector('.pagination')).toBeNull();
  });

  it('canonicalizes URL q on submit even when its normalized search term is unchanged', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/courses/search?q=%20REACT%20', GS02Page);

    http
      .expectOne((candidate) => candidate.params.get('q') === 'react')
      .flush(
        successEnvelope(
          coursePage({
            items: [course(101, 'React cơ bản')],
            pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
          }),
        ),
      );
    harness.fixture.detectChanges();
    const root = harness.routeNativeElement as HTMLElement;
    root
      .querySelector('form')!
      .dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    await harness.fixture.whenStable();

    http
      .expectOne((candidate) => candidate.params.get('q') === 'react')
      .flush(
        successEnvelope(
          coursePage({
            items: [course(101, 'React cơ bản')],
            pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
          }),
        ),
      );
    harness.fixture.detectChanges();

    expect(new URL(TestBed.inject(Location).path(), 'http://localhost').searchParams.get('q')).toBe(
      'react',
    );
  });

  it('submits normalized q, syncs it to the URL, and requests the next server page', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/courses/search', GS02Page);
    const root = harness.routeNativeElement as HTMLElement;
    const input = root.querySelector<HTMLInputElement>('#gs02-query');
    expect(input).not.toBeNull();

    input!.value = '  TypeScript  ';
    input!.dispatchEvent(new Event('input', { bubbles: true }));
    root
      .querySelector('form')!
      .dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    await harness.fixture.whenStable();

    const firstPage = http.expectOne(
      (candidate) =>
        candidate.url === '/api/v1/courses/search' &&
        candidate.params.get('q') === 'typescript' &&
        candidate.params.get('page') === '1',
    );
    firstPage.flush(
      successEnvelope(
        coursePage({
          items: Array.from({ length: 20 }, (_, index) =>
            course(100 + index, index === 0 ? 'TypeScript căn bản' : `Khóa học ${index + 1}`),
          ),
          pagination: { page: 1, size: 20, total: 21, total_pages: 2 },
        }),
      ),
    );
    harness.fixture.detectChanges();

    expect(new URL(TestBed.inject(Location).path(), 'http://localhost').searchParams.get('q')).toBe(
      'typescript',
    );
    const nextPage = root.querySelector<HTMLButtonElement>('.pagination button:last-child');
    expect(nextPage?.disabled).toBe(false);
    nextPage!.click();

    const secondRequest = http.expectOne(
      (candidate) =>
        candidate.url === '/api/v1/courses/search' &&
        candidate.params.get('q') === 'typescript' &&
        candidate.params.get('page') === '2',
    );
    expect(secondRequest.request.params.keys().sort()).toEqual(['page', 'q']);
    secondRequest.flush(
      successEnvelope(
        coursePage({
          items: [course(102, 'TypeScript nâng cao')],
          pagination: { page: 2, size: 20, total: 21, total_pages: 2 },
        }),
      ),
    );
    harness.fixture.detectChanges();

    expect(page.state()).toMatchObject({ status: 'ready', result: { pagination: { page: 2 } } });
    expect(root.textContent).toContain('TypeScript nâng cao');
    expect(root.textContent).toContain('Trang 2 / 2');

    input!.value = '  Vue  ';
    input!.dispatchEvent(new Event('input', { bubbles: true }));
    root
      .querySelector('form')!
      .dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    await harness.fixture.whenStable();
    const changedQuery = http.expectOne(
      (candidate) => candidate.params.get('q') === 'vue' && candidate.params.get('page') === '1',
    );
    changedQuery.flush(
      successEnvelope(
        coursePage({
          items: [course(103, 'Vue nhập môn')],
          pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
        }),
      ),
    );
    harness.fixture.detectChanges();
    expect(new URL(TestBed.inject(Location).path(), 'http://localhost').searchParams.get('q')).toBe(
      'vue',
    );
    expect(page.state()).toMatchObject({
      status: 'ready',
      query: 'vue',
      result: { pagination: { page: 1 } },
    });
  });

  it('shows an out-of-range response separately when results shrink between pages', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/courses/search?q=react', GS02Page);

    http
      .expectOne((candidate) => candidate.params.get('page') === '1')
      .flush(
        successEnvelope(
          coursePage({
            items: Array.from({ length: 20 }, (_, index) =>
              course(100 + index, index === 0 ? 'React cơ bản' : `Khóa học ${index + 1}`),
            ),
            pagination: { page: 1, size: 20, total: 21, total_pages: 2 },
          }),
        ),
      );
    harness.fixture.detectChanges();
    page.goToPage(2);

    http
      .expectOne((candidate) => candidate.params.get('page') === '2')
      .flush(
        successEnvelope(
          coursePage({
            items: [],
            pagination: { page: 2, size: 20, total: 10, total_pages: 1 },
          }),
        ),
      );
    harness.fixture.detectChanges();

    expect(page.state()).toEqual({
      status: 'out-of-range',
      query: 'react',
      page: 2,
      total: 10,
      totalPages: 1,
    });
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain(
      'Trang 2 không có khóa học',
    );

    (harness.routeNativeElement as HTMLElement)
      .querySelector<HTMLButtonElement>('.retry-button')
      ?.click();
    const refreshed = http.expectOne(
      (candidate) => candidate.params.get('q') === 'react' && candidate.params.get('page') === '1',
    );
    refreshed.flush(
      successEnvelope(
        coursePage({
          items: [course(101, 'React cơ bản')],
          pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
        }),
      ),
    );
    harness.fixture.detectChanges();
    expect(page.state()).toMatchObject({ status: 'ready', result: { pagination: { page: 1 } } });
  });

  it('keeps an empty result distinct from an API error', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/courses/search?q=missing', GS02Page);

    http
      .expectOne((candidate) => candidate.params.get('q') === 'missing')
      .flush(
        successEnvelope(
          coursePage({
            items: [],
            pagination: { page: 1, size: 20, total: 0, total_pages: 0 },
          }),
        ),
      );
    harness.fixture.detectChanges();
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain(
      'Không tìm thấy khóa học phù hợp',
    );
    expect(page.state()).toEqual({ status: 'no-results', query: 'missing' });
  });

  it('shows the error state for a failed search request', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/courses/search?q=react', GS02Page);

    http
      .expectOne((candidate) => candidate.params.get('q') === 'react')
      .flush({ message: 'temporary failure' }, { status: 500, statusText: 'Server error' });
    harness.fixture.detectChanges();

    expect(page.state()).toEqual({ status: 'error', query: 'react', page: 1 });
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain(
      'Không thể tải kết quả tìm kiếm lúc này.',
    );
    (harness.routeNativeElement as HTMLElement).querySelector<HTMLButtonElement>('.retry-button')?.click();
    http
      .expectOne((candidate) => candidate.params.get('q') === 'react' && candidate.params.get('page') === '1')
      .flush(
        successEnvelope(
          coursePage({
            items: [course(101, 'React đã tải lại')],
            pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
          }),
        ),
      );
    harness.fixture.detectChanges();
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain('React đã tải lại');
  });

  it('keeps rows but hides stale pagination when count and list disagree', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/courses/search?q=react', GS02Page);

    http
      .expectOne((candidate) => candidate.params.get('page') === '1')
      .flush(
        successEnvelope(
          coursePage({
            items: [course(101, 'React cơ bản')],
            pagination: { page: 1, size: 20, total: 2, total_pages: 1 },
          }),
        ),
      );
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('React cơ bản');
    expect(root.textContent).toContain('Số kết quả và danh sách trang chưa đồng nhất');
    expect(root.querySelector('.pagination')).toBeNull();
    expect(page.snapshotMismatch()).toBe(true);
    root.querySelector<HTMLButtonElement>('.primary-button')?.click();
    http
      .expectOne((candidate) => candidate.params.get('q') === 'react' && candidate.params.get('page') === '1')
      .flush(
        successEnvelope(
          coursePage({
            items: [course(101, 'React cơ bản'), course(102, 'React nâng cao')],
            pagination: { page: 1, size: 20, total: 2, total_pages: 1 },
          }),
        ),
      );
    harness.fixture.detectChanges();
    expect(page.snapshotMismatch()).toBe(false);
    expect(root.querySelector('.pagination')).toBeNull();
  });

  it('falls back to placeholder cover when search result thumbnail fails to load', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/courses/search?q=react', GS02Page);

    http
      .expectOne((candidate) => candidate.params.get('q') === 'react')
      .flush(
        successEnvelope(
          coursePage({
            items: [{ ...course(101, 'React cơ bản'), thumbnail_url: 'https://cdn.example.com/broken.png' }],
            pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
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

function course(id: number, title: string): GS02Course {
  return {
    id,
    title,
    description: 'Fundamentals of React',
    thumbnail_url: null,
    price: '49.90',
    status: 'PUBLISHED',
    mentor: { id: 7, full_name: 'Nguyen Van Mentor', avatar_url: null },
  };
}

function coursePage(data: {
  items: GS02Course[];
  pagination: GS02Pagination;
}): GS02CourseSearchPage {
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
