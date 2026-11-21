import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import type { StudentCourseProgress } from '../../shared/models/student-api.models';
import { ST09CourseOverviewService } from '../data-access/st09-course-overview.service';
import { ST09Page } from './st09-page';

describe('ST09Page', () => {
  it('loads progress only for an active course and keeps unsupported lesson selection gated', async () => {
    const data = {
      activeCourses: vi.fn(() => of(envelope({
        items: [{
          course_id: 42,
          name: 'Lập trình Web',
          enrollment_status: 'ACTIVE',
          enrolled_at: '2026-11-20T09:00:00Z',
        }],
        pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
      }))),
      progress: vi.fn(() => of(envelope<StudentCourseProgress>({
        course_id: 42,
        completed_lessons: 1,
        total_lessons: 4,
        progress_percent: 25,
        has_content: true,
      }))),
    };
    await TestBed.configureTestingModule({
      imports: [ST09Page],
      providers: [
        provideRouter([{ path: 'student/courses/:courseId', component: ST09Page }]),
        { provide: ST09CourseOverviewService, useValue: data },
      ],
    }).compileComponents();

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/courses/42', ST09Page);
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Lập trình Web');
    expect(root.textContent).toContain('25%');
    expect(root.textContent).toContain('Danh sách bài học hiện chưa khả dụng');
    expect(root.querySelectorAll('[data-lesson-id]')).toHaveLength(0);
    expect(root.textContent).not.toContain('API #');
    expect(data.activeCourses).toHaveBeenCalledWith(1);
    expect(data.progress).toHaveBeenCalledWith('42');
  });
});

function envelope<T>(data: T) {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Retrieved.',
    data,
    traceId: 'test-trace',
  };
}
