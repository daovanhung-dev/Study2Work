import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, Router, convertToParamMap, provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { Me09SubmissionsService } from '../data-access/me09-submissions.service';
import { ME09Page } from './me09-page';

describe('ME09Page', () => {
  const sampleCoursesEnvelope = {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'OK',
    data: {
      items: [{ id: 101, title: 'Kiến trúc Backend', status: 'PUBLISHED' }],
      pagination: { page: 1, size: 50, total: 1, total_pages: 1 },
    },
    meta: {},
    traceId: 'trace-me09-courses',
  };

  const sampleSubmissionsEnvelope = {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'OK',
    data: {
      items: [
        {
          id: 9001,
          assignment_id: 301,
          user_id: 7001,
          content: 'Bài làm học viên',
          files: [],
          status: 'SUBMITTED',
          submitted_at: '2026-11-12T08:00:00Z',
          score: null,
          feedback: null,
        },
      ],
      pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
    },
    meta: {},
    traceId: 'trace-me09-subs',
  };

  function setupTest(submissionsData = sampleSubmissionsEnvelope) {
    const serviceStub = {
      getMentorCourses: vi.fn().mockReturnValue(of(sampleCoursesEnvelope)),
      getSubmissions: vi.fn().mockReturnValue(of(submissionsData)),
    };

    TestBed.configureTestingModule({
      imports: [ME09Page],
      providers: [
        provideRouter([]),
        { provide: Me09SubmissionsService, useValue: serviceStub },
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: convertToParamMap({}),
              queryParamMap: convertToParamMap({ courseId: '101', status: 'SUBMITTED' }),
            },
          },
        },
      ],
    });

    return { serviceStub, router: TestBed.inject(Router) };
  }

  it('loads mentor courses (#46) and submissions (#54) and renders rows', () => {
    const { serviceStub } = setupTest();
    const fixture = TestBed.createComponent(ME09Page);
    fixture.detectChanges();

    expect(serviceStub.getMentorCourses).toHaveBeenCalledTimes(1);
    expect(serviceStub.getSubmissions).toHaveBeenCalledWith({
      course_id: 101,
      status: 'SUBMITTED',
      page: 1,
    });
    expect(fixture.componentInstance.screenState()).toBe('ready');

    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('#9001');
    expect(text).toContain('Assignment #301');
    expect(text).toContain('User #7001');
  });

  it('keeps keyword search input disabled per API #54 contract', () => {
    setupTest();
    const fixture = TestBed.createComponent(ME09Page);
    fixture.detectChanges();

    const searchInput = (fixture.nativeElement as HTMLElement).querySelector(
      '#search-keyword',
    ) as HTMLInputElement | null;
    expect(searchInput).not.toBeNull();
    expect(searchInput?.disabled).toBe(true);
  });

  it('navigates to ME-10 (/mentor/submissions/:submissionId) when opening a submission row', () => {
    const { router } = setupTest();
    const navSpy = vi.spyOn(router, 'navigate').mockResolvedValue(true);

    const fixture = TestBed.createComponent(ME09Page);
    fixture.detectChanges();

    fixture.componentInstance.openSubmissionDetail(9001);
    expect(navSpy).toHaveBeenCalledWith(['/mentor/submissions', 9001]);
  });
});
