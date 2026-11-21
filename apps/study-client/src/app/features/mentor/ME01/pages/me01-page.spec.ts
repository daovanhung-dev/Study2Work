import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of, throwError } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ME01DashboardService } from '../data-access/me01-dashboard.service';
import { ME01Page } from './me01-page';

describe('ME01Page', () => {
  let data: {
    courses: ReturnType<typeof vi.fn>;
    submissions: ReturnType<typeof vi.fn>;
    support: ReturnType<typeof vi.fn>;
  };

  beforeEach(async () => {
    data = {
      courses: vi.fn(() => of(envelope(page(courses, 4)))),
      submissions: vi.fn(() => of(envelope(page(submissions, 20)))),
      support: vi.fn(() => of(envelope(supportRequests))),
    };
    await TestBed.configureTestingModule({
      imports: [ME01Page],
      providers: [provideRouter([]), { provide: ME01DashboardService, useValue: data }],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('loads the three source-backed widgets independently and limits each dashboard preview to four rows', () => {
    const fixture = TestBed.createComponent(ME01Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(data.courses).toHaveBeenCalledOnce();
    expect(data.submissions).toHaveBeenCalledOnce();
    expect(data.support).toHaveBeenCalledOnce();
    expect(root.querySelectorAll('.me01-panel:nth-child(1) .mentor-list li')).toHaveLength(4);
    expect(root.querySelectorAll('.me01-panel:nth-child(2) .mentor-list li')).toHaveLength(4);
    expect(root.querySelectorAll('.me01-support .mentor-list li')).toHaveLength(4);
  });

  it('keeps a failed widget isolated and lets the user retry only that widget', () => {
    data.submissions
      .mockReturnValueOnce(throwError(() => new Error('temporary failure')))
      .mockReturnValueOnce(of(envelope(page(submissions, 20))));

    const fixture = TestBed.createComponent(ME01Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Không thể tải dữ liệu lúc này. Vui lòng thử lại.');
    expect(root.textContent).toContain('Khóa 1');
    expect(root.textContent).toContain('Yêu cầu #1');

    const retry = Array.from(root.querySelectorAll('button')).find((button) =>
      button.textContent?.includes('Tải lại bài nộp'),
    );
    if (!(retry instanceof HTMLButtonElement)) throw new Error('ME-01 submission retry is missing.');
    retry.click();
    fixture.detectChanges();

    expect(data.submissions).toHaveBeenCalledTimes(2);
    expect(data.courses).toHaveBeenCalledOnce();
    expect(data.support).toHaveBeenCalledOnce();
    expect(root.textContent).not.toContain('Không thể tải dữ liệu lúc này. Vui lòng thử lại.');
  });
});

const courses = Array.from({ length: 4 }, (_, index) => ({
  id: index + 1,
  title: `Khóa ${index + 1}`,
  description: null,
  thumbnail_url: null,
  price: '0.00',
  status: 'PUBLISHED',
  mentor: { id: 9, full_name: 'Mentor', avatar_url: null },
}));

const submissions = Array.from({ length: 8 }, (_, index) => ({
  id: index + 1,
  assignment_id: 41,
  user_id: 51 + index,
  content: 'Không hiển thị ở dashboard.',
  files: [],
  status: 'SUBMITTED',
  submitted_at: '2026-11-21T10:00:00Z',
  score: null,
  feedback: null,
}));

const supportRequests = Array.from({ length: 6 }, (_, index) => ({
  id: index + 1,
  course_id: 71,
  student: { id: 81 + index, full_name: `Student ${index + 1}`, avatar_url: null },
  status: 'OPEN',
  messages: [{
    id: 91 + index,
    author: { id: 81 + index, full_name: `Student ${index + 1}`, avatar_url: null },
    content: `Yêu cầu #${index + 1}`,
    attachments: [],
    created_at: '2026-11-21T10:00:00Z',
  }],
  created_at: '2026-11-21T10:00:00Z',
  resolved_at: null,
}));

function page<T>(items: T[], size: number) {
  return {
    items,
    pagination: { page: 1, size, total: items.length, total_pages: Math.ceil(items.length / size) },
  };
}

function envelope<T>(data: T) {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'OK',
    data,
    meta: {},
    traceId: 'me01-test',
  };
}
