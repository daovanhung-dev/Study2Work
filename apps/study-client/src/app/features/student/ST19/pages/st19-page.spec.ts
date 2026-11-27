import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ST19SubmissionService } from '../data-access/st19-submission.service';
import { ST19Page } from './st19-page';

describe('ST19Page', () => {
  let submission: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    submission = vi.fn().mockReturnValue(of(apiEnvelope(submissionData())));

    await TestBed.configureTestingModule({
      imports: [ST19Page],
      providers: [
        provideRouter([{ path: 'student/submissions/:submissionId', component: ST19Page }]),
        { provide: ST19SubmissionService, useValue: { submission } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('hides timestamp, grade, feedback, and file metadata while policy is unresolved', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/submissions/54', ST19Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(submission).toHaveBeenCalledExactlyOnceWith('54');
    expect(root.querySelector('h1')?.textContent).toContain('Chi tiết bài nộp');
    expect(root.textContent).toContain('Đã chấm');
    expect(root.textContent).toContain('My submitted answer');
    expect(root.querySelector('dt')?.textContent).toBe('Trạng thái');
    expect(root.querySelectorAll('dt')).toHaveLength(1);
    expect(root.textContent).not.toContain('Điểm');
    expect(root.textContent).not.toContain('95');
    expect(root.textContent).not.toContain('Phản hồi');
    expect(root.textContent).not.toContain('Great work.');
    expect(root.textContent).not.toContain('Tệp đính kèm');
    expect(root.textContent).not.toContain('private-report.pdf');
    expect(root.textContent).not.toContain('2026');
  });
});

function submissionData() {
  return {
    id: 54,
    assignment_id: 7,
    user_id: 19,
    content: 'My submitted answer',
    files: [
      {
        id: 88,
        name: 'private-report.pdf',
        url: 'https://files.example/private-report.pdf',
        content_type: 'application/pdf',
        size_bytes: 250,
        status: 'UPLOADED',
      },
    ],
    status: 'GRADED',
    submitted_at: '2026-11-27T12:00:00Z',
    score: '95',
    feedback: 'Great work.',
  };
}

function apiEnvelope<T>(data: T) {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Submission loaded.',
    data,
    meta: {},
    traceId: 'st19-test',
  };
}
