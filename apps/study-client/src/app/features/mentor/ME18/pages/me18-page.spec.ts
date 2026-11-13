import { HttpErrorResponse } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, Router } from '@angular/router';
import { of, throwError } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';
import { Me18AnalyticsService } from '../data-access/me18-analytics.service';
import { MentorCourseActivityAnalyticsDto } from '../models/me18-analytics.models';
import { ME18Page } from './me18-page';

const MOCK_ANALYTICS: MentorCourseActivityAnalyticsDto = {
  tracked_lesson_accesses: 42,
  students_with_activity: 15,
  last_activity_at: '2026-11-12T09:15:00Z',
};

describe('ME18Page', () => {
  function setup(courseIdParam: string | null = '10', serviceMock?: Partial<Me18AnalyticsService>) {
    const defaultService: Pick<Me18AnalyticsService, 'getCourseAnalytics'> = {
      getCourseAnalytics: vi.fn().mockReturnValue(of(MOCK_ANALYTICS)),
      ...serviceMock,
    };

    TestBed.configureTestingModule({
      imports: [ME18Page],
      providers: [
        provideRouter([]),
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: convertToParamMap(courseIdParam ? { courseId: courseIdParam } : {}),
            },
          },
        },
        { provide: Me18AnalyticsService, useValue: defaultService },
      ],
    });

    const fixture: ComponentFixture<ME18Page> = TestBed.createComponent(ME18Page);
    const router = TestBed.inject(Router);
    return { fixture, component: fixture.componentInstance, service: defaultService, router };
  }

  it('loads course analytics metrics on init for valid courseId', () => {
    const { fixture, component, service } = setup('10');
    fixture.detectChanges();

    expect(service.getCourseAnalytics).toHaveBeenCalledWith(10);
    expect(component.analytics()?.tracked_lesson_accesses).toBe(42);
    expect(component.analytics()?.students_with_activity).toBe(15);

    const el = fixture.nativeElement as HTMLElement;
    expect(el.querySelector('[data-testid="metric-tracked-accesses"]')?.textContent).toContain('42');
    expect(el.querySelector('[data-testid="metric-active-students"]')?.textContent).toContain('15');
    const exportBtn = el.querySelector('[data-testid="export-csv-btn"]') as HTMLButtonElement;
    expect(exportBtn.disabled).toBe(true);
  });

  it('shows invalid param error when courseId is not a positive integer', () => {
    const { fixture, component, service } = setup('invalid');
    fixture.detectChanges();

    expect(service.getCourseAnalytics).not.toHaveBeenCalled();
    expect(component.errorCode()).toBe('INVALID_COURSE_ID');
  });

  it('displays API error banner when analytics request fails', () => {
    const { fixture, component } = setup('10', {
      getCourseAnalytics: vi.fn().mockReturnValue(
        throwError(
          () =>
            new HttpErrorResponse({
              status: 404,
              error: { error: { code: 'COURSE_NOT_FOUND', message: 'Course not found' } },
            }),
        ),
      ),
    });
    fixture.detectChanges();

    expect(component.errorCode()).toBe('COURSE_NOT_FOUND');
    const banner = (fixture.nativeElement as HTMLElement).querySelector('[data-testid="error-banner"]');
    expect(banner?.textContent).toContain('COURSE_NOT_FOUND');
  });

  it('navigates back to ME-16 course progress page', () => {
    const { fixture, component, router } = setup('10');
    const navSpy = vi.spyOn(router, 'navigate').mockResolvedValue(true);
    fixture.detectChanges();

    component.backToProgress();
    expect(navSpy).toHaveBeenCalledWith(['/mentor/courses', 10, 'progress']);
  });
});
