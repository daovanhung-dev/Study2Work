import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, Router, convertToParamMap, provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { Me17StudentProgressService } from '../data-access/me17-student-progress.service';
import { ME17Page } from './me17-page';

describe('ME17Page', () => {
  const sampleStudentProgressEnvelope = {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'OK',
    data: {
      course_id: 101,
      student: { id: 3001, full_name: 'Trần Thị B', avatar_url: null },
      summary: {
        completed_lessons: 1,
        total_lessons: 2,
        progress_percent: 50,
      },
      lessons: [
        {
          lesson_id: 11,
          title: 'Bài 1: Giới thiệu kiến trúc',
          order: 1,
          progress_status: 'COMPLETED',
          progress_percent: 100,
          last_accessed_at: '2026-11-12T07:00:00Z',
          completed_at: '2026-11-12T07:30:00Z',
        },
        {
          lesson_id: 12,
          title: 'Bài 2: Thiết kế REST API',
          order: 2,
          progress_status: 'IN_PROGRESS',
          progress_percent: 40,
          last_accessed_at: '2026-11-12T08:00:00Z',
          completed_at: null,
        },
      ],
    },
    meta: {},
    traceId: 'trace-me17',
  };

  function setupTest(courseId = '101', studentId = '3001') {
    const serviceStub = {
      getStudentCourseProgress: vi.fn().mockReturnValue(of(sampleStudentProgressEnvelope)),
    };

    TestBed.configureTestingModule({
      imports: [ME17Page],
      providers: [
        provideRouter([]),
        { provide: Me17StudentProgressService, useValue: serviceStub },
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: convertToParamMap({ courseId, studentId }),
              queryParamMap: convertToParamMap({}),
            },
          },
        },
      ],
    });

    return { serviceStub, router: TestBed.inject(Router) };
  }

  it('loads student lesson progress via API #67 and renders summary + lessons table', () => {
    const { serviceStub } = setupTest('101', '3001');
    const fixture = TestBed.createComponent(ME17Page);
    fixture.detectChanges();

    expect(serviceStub.getStudentCourseProgress).toHaveBeenCalledWith(101, 3001);
    expect(fixture.componentInstance.screenState()).toBe('ready');

    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Trần Thị B');
    expect(text).toContain('Bài 1: Giới thiệu kiến trúc');
    expect(text).toContain('Bài 2: Thiết kế REST API');
  });

  it('navigates back to ME-16 (/mentor/courses/:courseId/progress)', () => {
    const { router } = setupTest('101', '3001');
    const navSpy = vi.spyOn(router, 'navigate').mockResolvedValue(true);

    const fixture = TestBed.createComponent(ME17Page);
    fixture.detectChanges();

    fixture.componentInstance.backToCourseProgress();
    expect(navSpy).toHaveBeenCalledWith(['/mentor/courses', 101, 'progress']);
  });
});
