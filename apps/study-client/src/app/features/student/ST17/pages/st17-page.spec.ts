import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ST17AssignmentService } from '../data-access/st17-assignment.service';
import { ST17Page } from './st17-page';

describe('ST17Page', () => {
  let assignment: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    assignment = vi.fn().mockReturnValue(of(apiEnvelope(assignmentData())));

    await TestBed.configureTestingModule({
      imports: [ST17Page],
      providers: [
        provideRouter([{ path: 'student/assignments/:assignmentId', component: ST17Page }]),
        { provide: ST17AssignmentService, useValue: { assignment } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('hides unresolved deadline, score, course identity, and submission eligibility', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/assignments/42', ST17Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(assignment).toHaveBeenCalledExactlyOnceWith('42');
    expect(root.querySelector('h1')?.textContent).toContain('Assignment');
    expect(root.textContent).toContain('Write a short response.');
    expect(root.textContent).not.toContain('Hạn nộp');
    expect(root.textContent).not.toContain('Điểm tối đa');
    expect(root.textContent).not.toContain('Khóa học liên quan');
    expect(root.textContent).not.toContain('November 30, 2026');
    expect(root.textContent).not.toContain('Soạn và nộp bài');
    expect(root.querySelector('a[href="/student/assignments/42/submit"]')).toBeNull();
  });
});

function assignmentData() {
  return {
    id: 42,
    course_id: 7,
    title: 'Assignment',
    description: 'Write a short response.',
    due_at: '2026-11-30T12:00:00Z',
    max_score: 95,
  };
}

function apiEnvelope<T>(data: T) {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Assignment loaded.',
    data,
    meta: {},
    traceId: 'st17-test',
  };
}
