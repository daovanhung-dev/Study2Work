import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { ST08CoursesService } from '../data-access/st08-courses.service';
import { ST08Page } from './st08-page';

describe('ST08Page', () => {
  it('filters to active enrollments and makes the matching request', async () => {
    const data = {
      courses: vi
        .fn()
        .mockReturnValueOnce(of(envelope(page([activeCourse, completedCourse], 2))))
        .mockReturnValueOnce(of(envelope(page([activeCourse], 1)))),
    };
    await TestBed.configureTestingModule({
      imports: [ST08Page],
      providers: [provideRouter([]), { provide: ST08CoursesService, useValue: data }],
    }).compileComponents();

    const fixture = TestBed.createComponent(ST08Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Lập trình Web');
    expect(root.textContent).toContain('Thiết kế giao diện');
    expect(data.courses).toHaveBeenNthCalledWith(1, 1, undefined);

    const activeFilter = Array.from(root.querySelectorAll('button')).find((button) =>
      button.textContent?.includes('Đang học'),
    );
    activeFilter!.click();
    fixture.detectChanges();

    expect(data.courses).toHaveBeenNthCalledWith(2, 1, 'ACTIVE');
    expect(root.textContent).toContain('Lập trình Web');
    expect(root.textContent).not.toContain('Thiết kế giao diện');
  });
});

const activeCourse = {
  course_id: 42,
  name: 'Lập trình Web',
  enrollment_status: 'ACTIVE',
  enrolled_at: '2026-11-20T09:00:00Z',
  course_status: 'PUBLISHED',
};

const completedCourse = {
  course_id: 12,
  name: 'Thiết kế giao diện',
  enrollment_status: 'COMPLETED',
  enrolled_at: '2026-11-19T09:00:00Z',
  course_status: 'PUBLISHED',
};

function page<T>(items: T[], total: number) {
  return {
    items,
    pagination: {
      page: 1,
      size: 20,
      total,
      total_pages: total === 0 ? 0 : Math.ceil(total / 20),
    },
  };
}

function envelope<T>(data: T) {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Retrieved.',
    data,
    traceId: 'test-trace',
  };
}
