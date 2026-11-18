import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { StudentCoursesService } from '../data-access/ST-08-courses.service';
import { StudentCoursesPage } from './ST-08-courses-page';

describe('ST-08 courses page', () => {
  async function render(getCourses: ReturnType<typeof vi.fn>) {
    await TestBed.configureTestingModule({
      imports: [StudentCoursesPage],
      providers: [{ provide: StudentCoursesService, useValue: { getCourses } }],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentCoursesPage);
    fixture.detectChanges();
    return fixture;
  }

  it('shows the DD empty state when API #20 returns no enrolled courses', async () => {
    const getCourses = vi.fn(() => of({
      items: [],
      pagination: { page: 1, size: 10, total: 0, total_pages: 0 },
    }));
    const fixture = await render(getCourses);

    expect(getCourses).toHaveBeenCalledWith(1);
    expect(fixture.componentInstance.state().kind).toBe('empty');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Chưa có khóa học để hiển thị.');
    expect((fixture.nativeElement as HTMLElement).querySelector<HTMLAnchorElement>('.btn-primary')?.getAttribute('href')).toBe('/student/progress');
  });

  it('renders real course data and avoids invented progress values', async () => {
    const getCourses = vi.fn(() => of({
      items: [{ course_id: 42, name: 'Khóa Angular', description: 'Kiến thức cơ bản', thumbnail_url: null,
        enrollment_status: 'ACTIVE', enrolled_at: '2026-11-18T00:00:00Z' }],
      pagination: { page: 1, size: 10, total: 1, total_pages: 1 },
    }));
    const fixture = await render(getCourses);
    const element = fixture.nativeElement as HTMLElement;

    expect(element.textContent).toContain('Khóa Angular');
    expect(element.textContent).toContain('ACTIVE');
    expect(element.textContent).toContain('Chưa có dữ liệu tiến độ từ API.');
    expect(element.querySelector<HTMLAnchorElement>('.course-link')?.getAttribute('href')).toBe('/student/courses/42');
    expect(element.textContent).not.toContain('0%');
  });

  it('offers retry when the API fails', async () => {
    const getCourses = vi.fn(() => throwError(() => new HttpErrorResponse({ status: 500 })));
    const fixture = await render(getCourses);
    const element = fixture.nativeElement as HTMLElement;

    expect(fixture.componentInstance.state().kind).toBe('error');
    expect(element.textContent).toContain('HTTP 500');
    element.querySelector<HTMLButtonElement>('button.btn-primary')?.click();
    expect(getCourses).toHaveBeenCalledTimes(2);
  });
});
