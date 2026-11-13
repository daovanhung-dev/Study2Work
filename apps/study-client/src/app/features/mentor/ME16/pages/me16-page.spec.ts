import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, Router, convertToParamMap, provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { Me16ProgressService } from '../data-access/me16-progress.service';
import { ME16Page } from './me16-page';

describe('ME16Page', () => {
  const sampleProgressEnvelope = {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'OK',
    data: {
      items: [
        {
          student: { id: 3001, full_name: 'Trần Thị B', avatar_url: null },
          completed_lessons: 8,
          total_lessons: 10,
          progress_percent: 80,
        },
      ],
      pagination: { page: 1, size: 1, total: 1, total_pages: 1 },
    },
    meta: {},
    traceId: 'trace-me16',
  };

  function setupTest(courseId = '101') {
    const serviceStub = {
      getCourseProgress: vi.fn().mockReturnValue(of(sampleProgressEnvelope)),
    };

    TestBed.configureTestingModule({
      imports: [ME16Page],
      providers: [
        provideRouter([]),
        { provide: Me16ProgressService, useValue: serviceStub },
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: convertToParamMap({ courseId }),
              queryParamMap: convertToParamMap({}),
            },
          },
        },
      ],
    });

    return { serviceStub, router: TestBed.inject(Router) };
  }

  it('loads course roster progress via API #65 and displays student row', () => {
    const { serviceStub } = setupTest('101');
    const fixture = TestBed.createComponent(ME16Page);
    fixture.detectChanges();

    expect(serviceStub.getCourseProgress).toHaveBeenCalledWith(101);
    expect(fixture.componentInstance.screenState()).toBe('ready');

    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Trần Thị B');
    expect(text).toContain('8 / 10 bài');
    expect(text).toContain('80%');
  });

  it('navigates to ME-17 (/mentor/courses/:courseId/students/:studentId/progress)', () => {
    const { router } = setupTest('101');
    const navSpy = vi.spyOn(router, 'navigate').mockResolvedValue(true);

    const fixture = TestBed.createComponent(ME16Page);
    fixture.detectChanges();

    fixture.componentInstance.openStudentDetail(3001);
    expect(navSpy).toHaveBeenCalledWith(['/mentor/courses', 101, 'students', 3001, 'progress']);
  });

  it('navigates to ME-18 (/mentor/courses/:courseId/analytics)', () => {
    const { router } = setupTest('101');
    const navSpy = vi.spyOn(router, 'navigate').mockResolvedValue(true);

    const fixture = TestBed.createComponent(ME16Page);
    fixture.detectChanges();

    fixture.componentInstance.openCourseAnalytics();
    expect(navSpy).toHaveBeenCalledWith(['/mentor/courses', 101, 'analytics']);
  });
});
