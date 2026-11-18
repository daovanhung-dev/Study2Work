import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { of, throwError, type Observable } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { StudentCourseOverviewService } from '../data-access/ST-09-course-overview.service';
import type { VerifiedCourseOverview } from '../models/ST-09-course-overview.models';
import { StudentCourseOverviewPage } from './ST-09-course-overview-page';

async function renderPage(courseId?: string, getOverview: (courseId: string) => Observable<VerifiedCourseOverview | null> = vi.fn(() => of(null))) {
  const paramMap = convertToParamMap(courseId === undefined ? {} : { courseId });
  await TestBed.configureTestingModule({
    imports: [StudentCourseOverviewPage],
    providers: [
      { provide: ActivatedRoute, useValue: { paramMap: of(paramMap), snapshot: { paramMap } } },
      { provide: StudentCourseOverviewService, useValue: { getOverview } },
    ],
  }).compileComponents();
  const fixture = TestBed.createComponent(StudentCourseOverviewPage);
  fixture.detectChanges();
  return { fixture, getOverview };
}

describe('ST-09 course overview page', () => {
  it('does not request an overview without a courseId', async () => {
    const { fixture, getOverview } = await renderPage();
    expect(fixture.componentInstance.state().kind).toBe('missing-context');
    expect(getOverview).not.toHaveBeenCalled();
  });

  it.each(['abc', '0', '-1', '01', '9223372036854775808'])(
    'rejects invalid course ID %s before requesting data', async (courseId) => {
      const { fixture, getOverview } = await renderPage(courseId);
      expect(fixture.componentInstance.state().kind).toBe('missing-context');
      expect(getOverview).not.toHaveBeenCalled();
    },
  );

  it('keeps lesson access blocked when no active enrollment is found', async () => {
    const { fixture, getOverview } = await renderPage('1');
    expect(getOverview).toHaveBeenCalledWith('1');
    expect(fixture.componentInstance.state().kind).toBe('not-enrolled');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Bạn chưa ghi danh khóa học này.');
    expect((fixture.nativeElement as HTMLElement).querySelector<HTMLButtonElement>('button.btn-primary')?.disabled).toBe(true);
  });

  it('renders verified data without offering lesson playback', async () => {
    const getOverview = vi.fn(() => of({ courseId: 42, name: 'Khóa Angular', completedLessons: 2,
      totalLessons: 4, progressPercent: 50, publicLessons: [{ id: 3, title: 'Bài mở đầu', order: 1 }] }));
    const { fixture } = await renderPage('42', getOverview);
    const element = fixture.nativeElement as HTMLElement;
    expect(fixture.componentInstance.state().kind).toBe('ready');
    expect(element.textContent).toContain('Khóa Angular');
    expect(element.textContent).toContain('Bài mở đầu');
    expect(element.querySelector('progress')?.value).toBe(50);
    expect(element.querySelector<HTMLButtonElement>('button.btn-primary')?.disabled).toBe(true);
  });

  it('blocks data presentation when an API fails', async () => {
    const getOverview = vi.fn(() => throwError(() => new HttpErrorResponse({ status: 500 })));
    const { fixture } = await renderPage('42', getOverview);
    expect(fixture.componentInstance.state().kind).toBe('blocked');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('HTTP 500');
  });
});
