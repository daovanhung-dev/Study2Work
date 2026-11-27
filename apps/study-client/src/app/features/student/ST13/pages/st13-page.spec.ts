import { HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { Subject, of, throwError } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ST13QuizService } from '../data-access/st13-quiz.service';
import type { StudentQuiz, StudentQuizAttempt } from '../../shared/models/student-api.models';
import { ST13Page } from './st13-page';

@Component({ standalone: true, template: '<p>Attempt route reached</p>' })
class AttemptRouteStub {}

describe('ST13Page', () => {
  let loadQuiz: ReturnType<typeof vi.fn>;
  let startAttempt: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    loadQuiz = vi.fn(() => of(apiEnvelope(quiz(), 'DESIGN_RESOURCE_RETRIEVED')));
    startAttempt = vi.fn(() => of(apiEnvelope(attempt(), 'DESIGN_RESOURCE_CREATED')));

    await TestBed.configureTestingModule({
      imports: [ST13Page, AttemptRouteStub],
      providers: [
        provideRouter([
          { path: 'student/quizzes/:quizId/attempts/:attemptId', component: AttemptRouteStub },
          { path: 'student/quizzes/:quizId', component: ST13Page },
        ]),
        { provide: ST13QuizService, useValue: { quiz: loadQuiz, start: startAttempt } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('loads the quiz without creating an attempt', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/quizzes/28', ST13Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(loadQuiz).toHaveBeenCalledExactlyOnceWith('28');
    expect(startAttempt).not.toHaveBeenCalled();
    expect(root.querySelector('h1')?.textContent).toContain('Bài kiểm tra an toàn');
    expect(root.textContent).toContain('1 câu hỏi');
    expect(root.querySelector<HTMLButtonElement>('button[type="button"]')?.disabled).toBe(false);
  });

  it('creates one attempt only after Start and routes with the returned ID', async () => {
    const pendingStart = new Subject<ReturnType<typeof apiEnvelope<StudentQuizAttempt>>>();
    startAttempt.mockReturnValueOnce(pendingStart.asObservable());

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/quizzes/28', ST13Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const startButton = root.querySelector<HTMLButtonElement>('button[type="button"]');
    expect(startButton).not.toBeNull();
    startButton?.click();
    harness.fixture.detectChanges();

    expect(startAttempt).toHaveBeenCalledExactlyOnceWith('28');
    expect(startButton?.disabled).toBe(true);
    expect(TestBed.inject(Router).url).toBe('/student/quizzes/28');

    pendingStart.next(apiEnvelope(attempt(), 'DESIGN_RESOURCE_CREATED'));
    pendingStart.complete();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(TestBed.inject(Router).url).toBe('/student/quizzes/28/attempts/501');
    expect(harness.routeNativeElement?.textContent).toContain('Attempt route reached');
    expect(startAttempt).toHaveBeenCalledTimes(1);
  });

  it('locks Start when #29 success does not return an attempt for this quiz', async () => {
    const pendingStart = new Subject<ReturnType<typeof apiEnvelope<StudentQuizAttempt>>>();
    startAttempt.mockReturnValueOnce(pendingStart.asObservable());

    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/student/quizzes/28', ST13Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    root.querySelector<HTMLButtonElement>('button[type="button"]')?.click();
    harness.fixture.detectChanges();
    pendingStart.next(
      apiEnvelope({ ...attempt(), quiz_id: 99 }, 'DESIGN_RESOURCE_CREATED'),
    );
    pendingStart.complete();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const startButton = root.querySelector<HTMLButtonElement>('button[type="button"]');
    expect(page.createdAttemptId()).toBeNull();
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Không xác định được lượt làm nào để tiếp tục.',
    );
    expect(startButton?.disabled).toBe(true);
    startButton?.click();
    expect(startAttempt).toHaveBeenCalledTimes(1);
    expect(TestBed.inject(Router).url).toBe('/student/quizzes/28');
  });

  it('locks out a second create after a transport-ambiguous #29 error', async () => {
    const pendingStart = new Subject<ReturnType<typeof apiEnvelope<StudentQuizAttempt>>>();
    startAttempt.mockReturnValueOnce(pendingStart.asObservable());

    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/student/quizzes/28', ST13Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    root.querySelector<HTMLButtonElement>('button[type="button"]')?.click();
    harness.fixture.detectChanges();
    pendingStart.error(new HttpErrorResponse({ status: 0, statusText: 'Network error' }));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const startButton = root.querySelector<HTMLButtonElement>('button[type="button"]');
    expect(page.startBlockedQuizId()).toBe('28');
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Không xác định được lượt làm nào để tiếp tục.',
    );
    expect(startButton?.disabled).toBe(true);
    startButton?.click();
    expect(startAttempt).toHaveBeenCalledTimes(1);
  });

  it('does not repeat #29 after an active-attempt conflict with no recovery ID', async () => {
    const pendingStart = new Subject<ReturnType<typeof apiEnvelope<StudentQuizAttempt>>>();
    startAttempt.mockReturnValueOnce(pendingStart.asObservable());

    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/student/quizzes/28', ST13Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    root.querySelector<HTMLButtonElement>('button[type="button"]')?.click();
    harness.fixture.detectChanges();
    pendingStart.error(new HttpErrorResponse({ status: 409, statusText: 'Conflict' }));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(page.startBlockedQuizId()).toBe('28');
    expect(root.querySelector<HTMLButtonElement>('button[type="button"]')?.disabled).toBe(true);
    root.querySelector<HTMLButtonElement>('button[type="button"]')?.click();
    expect(startAttempt).toHaveBeenCalledTimes(1);
    expect(page.createdAttemptId()).toBeNull();
  });

  it('offers a quiz retry and recovers after #28 fails', async () => {
    loadQuiz
      .mockReturnValueOnce(throwError(() => new Error('temporary failure')))
      .mockReturnValueOnce(of(apiEnvelope(quiz(), 'DESIGN_RESOURCE_RETRIEVED')));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/quizzes/28', ST13Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent?.trim()).toBeTruthy();
    root.querySelector<HTMLButtonElement>('.api-error button')?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(loadQuiz).toHaveBeenCalledTimes(2);
    expect(startAttempt).not.toHaveBeenCalled();
    expect(root.querySelector('h1')?.textContent).toContain('Bài kiểm tra an toàn');
    expect(root.querySelector('[role="alert"]')).toBeNull();
  });
});

function quiz(): StudentQuiz {
  return {
    id: 28,
    course_id: 4,
    title: 'Bài kiểm tra an toàn',
    duration_minutes: 15,
    passing_score: '70',
    questions: [
      {
        id: 31,
        text: 'Xác thực hai bước',
        type: 'MULTIPLE_CHOICE',
        choices: [
          { id: 101, choice_text: 'Bật xác thực hai bước' },
          { id: 102, choice_text: 'Chia sẻ mã xác thực' },
        ],
      },
    ],
  };
}

function attempt(): StudentQuizAttempt {
  return {
    id: 501,
    quiz_id: 28,
    status: 'IN_PROGRESS',
    started_at: '2026-11-27T02:00:00Z',
    answers: [],
  };
}

function apiEnvelope<T>(data: T, businessCode: string) {
  return {
    success: true,
    businessCode,
    message: 'Quiz data loaded.',
    data,
    meta: {},
    traceId: 'st13-test',
  };
}
