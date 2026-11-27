import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ST21CourseProgressService } from '../data-access/st21-course-progress.service';
import { ST21Page } from './st21-page';

describe('ST21Page', () => {
  let progress: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    progress = vi.fn().mockReturnValue(of(apiEnvelope(courseProgress())));

    await TestBed.configureTestingModule({
      imports: [ST21Page],
      providers: [
        provideRouter([{ path: 'student/progress/:courseId', component: ST21Page }]),
        { provide: ST21CourseProgressService, useValue: { progress } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('renders the API-backed aggregate progress without inventing a lesson timeline', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/progress/42', ST21Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(progress).toHaveBeenCalledExactlyOnceWith('42');
    expect(root.querySelector('h1')?.textContent).toContain('Tiến độ khóa học');
    expect(root.textContent).toContain('40%');
    expect(root.textContent).toContain('2 / 5 bài hoàn thành');
    expect(root.querySelector('[role="progressbar"]')?.getAttribute('aria-valuenow')).toBe('40');
    expect(root.textContent).toContain('Chi tiết tiến độ từng bài học hiện chưa khả dụng.');
  });

  it('does not call API #37 for an invalid course route ID', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/progress/not-a-number', ST21Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(progress).not.toHaveBeenCalled();
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Không tìm thấy khóa học này.',
    );
    expect(root.querySelector('button')).toBeNull();
  });
});

function courseProgress() {
  return {
    course_id: 42,
    completed_lessons: 2,
    total_lessons: 5,
    progress_percent: 40,
    has_content: true,
  };
}

function apiEnvelope<T>(data: T) {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Course progress loaded.',
    data,
    meta: {},
    traceId: 'st21-test',
  };
}
