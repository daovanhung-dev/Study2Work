import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import type { ComponentFixture } from '@angular/core/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { GS05CourseReviewsPage, GS05ReviewResponse } from '../models/gs05-reviews.models';
import { GS05Page } from './gs05-page';

describe('GS05Page', () => {
  let fixture: ComponentFixture<GS05Page>;
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GS05Page],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('maps source-backed review/reply content and requests bounded pages without auth', () => {
    fixture = TestBed.createComponent(GS05Page);
    fixture.componentRef.setInput('courseId', '9223372036854775807');
    fixture.detectChanges();

    const firstPage = http.expectOne('/api/v1/courses/9223372036854775807/reviews?page=1');
    expect(firstPage.request.method).toBe('GET');
    expect(firstPage.request.headers.has('Authorization')).toBe(false);
    firstPage.flush(
      successEnvelope(
        reviewsPage(
          Array.from({ length: 20 }, (_, index) =>
            review({
              id: 45 + index,
              content: index === 0 ? 'Nội dung đánh giá công khai.' : `Đánh giá ${index + 1}`,
              title: index === 0 ? 'Tiêu đề chưa được duyệt' : null,
              comments:
                index === 0
                  ? [
                      {
                        id: 78,
                        discussion_id: 45,
                        content: 'Phản hồi công khai.',
                        author: { id: 8, full_name: 'Tran An', avatar_url: null },
                        created_at: '2026-11-17T00:00:00Z',
                      },
                    ]
                  : [],
            }),
          ),
          1,
          2,
        ),
      ),
    );
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Nguyen Binh');
    expect(root.textContent).toContain('Nội dung đánh giá công khai.');
    expect(root.textContent).toContain('Tran An');
    expect(root.textContent).toContain('Phản hồi công khai.');
    expect(root.textContent).toContain('Trang 1 / 2');
    expect(root.textContent).not.toContain('Tiêu đề chưa được duyệt');
    expect(root.textContent).not.toContain('ACTIVE');
    expect(root.textContent).not.toContain('2026-11-17');

    const reviewList = root.querySelector<HTMLElement>(
      '[role="list"][aria-label="Danh sách đánh giá và thảo luận"]',
    );
    expect(reviewList?.querySelectorAll(':scope > [role="listitem"]').length).toBe(20);
    const replyList = reviewList?.querySelector<HTMLElement>(
      '[role="list"][aria-label="Phản hồi"]',
    );
    expect(replyList?.querySelectorAll(':scope > [role="listitem"]').length).toBe(1);

    const paginationButtons = root.querySelectorAll<HTMLButtonElement>('.pagination button');
    expect(paginationButtons[0]?.disabled).toBe(true);
    expect(paginationButtons[1]?.disabled).toBe(false);

    paginationButtons[1]?.click();
    fixture.detectChanges();
    const secondPage = http.expectOne('/api/v1/courses/9223372036854775807/reviews?page=2');
    expect(secondPage.request.headers.has('Authorization')).toBe(false);
    secondPage.flush(successEnvelope(reviewsPage([review({ content: 'Trang hai.' })], 2, 2)));
    fixture.detectChanges();

    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Trang 2 / 2');
    const secondPageButtons = (
      fixture.nativeElement as HTMLElement
    ).querySelectorAll<HTMLButtonElement>('.pagination button');
    expect(secondPageButtons[0]?.disabled).toBe(false);
    expect(secondPageButtons[1]?.disabled).toBe(true);
    secondPageButtons[0]?.click();
    fixture.detectChanges();
    http
      .expectOne('/api/v1/courses/9223372036854775807/reviews?page=1')
      .flush(successEnvelope(reviewsPage([review({ content: 'Quay lại trang một.' })], 1, 2)));
    fixture.detectChanges();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Quay lại trang một.');
  });

  it('shows an empty state for an empty response page', () => {
    fixture = TestBed.createComponent(GS05Page);
    fixture.componentRef.setInput('courseId', '42');
    fixture.detectChanges();
    http
      .expectOne('/api/v1/courses/42/reviews?page=1')
      .flush(successEnvelope(reviewsPage([], 1, 0)));
    fixture.detectChanges();

    expect((fixture.nativeElement as HTMLElement).textContent).toContain(
      'Chưa có đánh giá hoặc thảo luận công khai.',
    );
  });

  it('shows not-found for a 404 response', () => {
    fixture = TestBed.createComponent(GS05Page);
    fixture.componentRef.setInput('courseId', '404');
    fixture.detectChanges();
    http
      .expectOne('/api/v1/courses/404/reviews?page=1')
      .flush({}, { status: 404, statusText: 'Not Found' });
    fixture.detectChanges();

    expect((fixture.nativeElement as HTMLElement).textContent).toContain(
      'Không tìm thấy nội dung đánh giá của khóa học này.',
    );
  });

  it('shows a safe error state for a failed request', () => {
    fixture = TestBed.createComponent(GS05Page);
    fixture.componentRef.setInput('courseId', '42');
    fixture.detectChanges();
    http
      .expectOne('/api/v1/courses/42/reviews?page=1')
      .flush({ message: 'private backend detail' }, { status: 500, statusText: 'Server Error' });
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Chưa thể tải đánh giá và thảo luận. Vui lòng thử lại sau.');
    expect(root.textContent).not.toContain('private backend detail');
    root.querySelector<HTMLButtonElement>('.retry-button')?.click();
    http
      .expectOne('/api/v1/courses/42/reviews?page=1')
      .flush(successEnvelope(reviewsPage([], 1, 0)));
    fixture.detectChanges();
    expect(root.textContent).toContain('Chưa có đánh giá hoặc thảo luận công khai.');
  });

  it('keeps returned reviews and hides stale pagination after a count/list mismatch', () => {
    fixture = TestBed.createComponent(GS05Page);
    fixture.componentRef.setInput('courseId', '42');
    fixture.detectChanges();

    http
      .expectOne('/api/v1/courses/42/reviews?page=1')
      .flush(successEnvelope(reviewsPage([review({ content: 'Đánh giá còn dùng được.' })], 1, 2)));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Đánh giá còn dùng được.');
    expect(root.textContent).toContain('Số đánh giá và danh sách trang chưa đồng nhất.');
    expect(root.querySelector('.pagination')).toBeNull();
    root.querySelector<HTMLButtonElement>('.retry-button')?.click();

    http
      .expectOne('/api/v1/courses/42/reviews?page=1')
      .flush(
        successEnvelope(
          reviewsPage(
            Array.from({ length: 20 }, (_, index) => review({ id: 45 + index })),
            1,
            2,
          ),
        ),
      );
    fixture.detectChanges();
    expect(root.querySelector('.pagination')).not.toBeNull();
  });
});

function review(overrides: Partial<GS05ReviewResponse> = {}): GS05ReviewResponse {
  return {
    id: 45,
    course_id: 42,
    title: null,
    content: 'Đánh giá mặc định.',
    author: { id: 5, full_name: 'Nguyen Binh', avatar_url: null },
    status: 'ACTIVE',
    created_at: '2026-11-17T00:00:00Z',
    comments: [],
    ...overrides,
  };
}

function reviewsPage(
  items: GS05ReviewResponse[],
  page: number,
  totalPages: number,
): GS05CourseReviewsPage {
  return {
    items,
    pagination: {
      page,
      size: 20,
      total: totalPages === 0 ? 0 : totalPages === 1 ? items.length : 21,
      total_pages: totalPages,
    },
  };
}

function successEnvelope<T>(data: T): ApiEnvelope<T> {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'ok',
    data,
    meta: {},
    traceId: 'gs05-test',
  };
}
