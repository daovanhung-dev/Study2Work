import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { Subject, of, throwError } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ST14AttemptService } from '../data-access/st14-attempt.service';
import type {
  StudentQuiz,
  StudentQuizAnswer,
  StudentQuizAttempt,
} from '../../shared/models/student-api.models';
import { ST14Page } from './st14-page';

describe('ST14Page', () => {
  let loadQuiz: ReturnType<typeof vi.fn>;
  let saveAnswer: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    loadQuiz = vi.fn(() => of(apiEnvelope(quiz(), 'DESIGN_RESOURCE_RETRIEVED')));
    saveAnswer = vi.fn((_attemptId: string, _questionId: number, _choiceIds: number[] | null) =>
      of(apiEnvelope(attempt([{ question_id: 31, choice_ids: [101] }]), 'DESIGN_RESOURCE_UPDATED')),
    );

    await TestBed.configureTestingModule({
      imports: [ST14Page],
      providers: [
        provideRouter([
          { path: 'student/quizzes/:quizId/attempts/:attemptId', component: ST14Page },
        ]),
        { provide: ST14AttemptService, useValue: { quiz: loadQuiz, save: saveAnswer } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('loads the route quiz without creating an attempt or saving an answer', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/quizzes/28/attempts/501', ST14Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(loadQuiz).toHaveBeenCalledExactlyOnceWith('28');
    expect(saveAnswer).not.toHaveBeenCalled();
    expect(root.textContent).toContain('Bài kiểm tra an toàn');
    expect(root.textContent).toContain('Quy tắc bảo mật');
    expect(root.textContent).toContain('Câu trả lời chưa thể khôi phục nếu bạn tải lại trang.');
    expect(root.querySelectorAll('input[type="checkbox"]')).toHaveLength(2);
  });

  it('waits for #30 and uses the returned answer state before announcing a save', async () => {
    const pendingSave = new Subject<ReturnType<typeof apiEnvelope<StudentQuizAttempt>>>();
    saveAnswer.mockReturnValueOnce(pendingSave.asObservable());

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/quizzes/28/attempts/501', ST14Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const choices = root.querySelectorAll<HTMLInputElement>('input[type="checkbox"]');
    expect(choices).toHaveLength(2);
    const choice = choices.item(0);
    choice.checked = true;
    choice.dispatchEvent(new Event('change', { bubbles: true }));
    harness.fixture.detectChanges();

    expect(saveAnswer).toHaveBeenCalledExactlyOnceWith('501', 31, [101]);
    expect(choice.disabled).toBe(true);
    expect(root.querySelector('[role="status"]')?.textContent).toContain('Đang lưu câu trả lời');
    expect(root.querySelector('.api-actions a')?.getAttribute('aria-disabled')).toBe('true');

    pendingSave.next(
      apiEnvelope(attempt([{ question_id: 31, choice_ids: [101] }]), 'DESIGN_RESOURCE_UPDATED'),
    );
    pendingSave.complete();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(choice.checked).toBe(true);
    expect(root.querySelector('[role="status"]')?.textContent).toContain('Câu trả lời đã được lưu.');
    expect(root.querySelector('.api-actions a')?.getAttribute('aria-disabled')).toBe('false');
  });

  it('rolls back the optimistic selection when #30 returns a different attempt', async () => {
    const invalidSave = new Subject<ReturnType<typeof apiEnvelope<StudentQuizAttempt>>>();
    saveAnswer.mockReturnValueOnce(invalidSave.asObservable());

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/quizzes/28/attempts/501', ST14Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const choice = root.querySelector<HTMLInputElement>('input[type="checkbox"]');
    expect(choice).not.toBeNull();
    if (choice) {
      choice.checked = true;
      choice.dispatchEvent(new Event('change', { bubbles: true }));
    }
    harness.fixture.detectChanges();

    expect(choice?.checked).toBe(true);
    invalidSave.next(
      apiEnvelope(
        { ...attempt([{ question_id: 31, choice_ids: [101] }]), id: 502 },
        'DESIGN_RESOURCE_UPDATED',
      ),
    );
    invalidSave.complete();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(saveAnswer).toHaveBeenCalledExactlyOnceWith('501', 31, [101]);
    expect(root.querySelector<HTMLInputElement>('input[type="checkbox"]')?.checked).toBe(false);
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Thông tin lượt làm chưa hợp lệ.',
    );
    expect(root.querySelector('.api-actions a')?.getAttribute('aria-disabled')).toBe('true');
  });

  it('offers a quiz retry and recovers after #28 fails', async () => {
    loadQuiz
      .mockReturnValueOnce(throwError(() => new Error('temporary failure')))
      .mockReturnValueOnce(of(apiEnvelope(quiz(), 'DESIGN_RESOURCE_RETRIEVED')));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/quizzes/28/attempts/501', ST14Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent?.trim()).toBeTruthy();
    root.querySelector<HTMLButtonElement>('.api-error button')?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(loadQuiz).toHaveBeenCalledTimes(2);
    expect(root.textContent).toContain('Bài kiểm tra an toàn');
    expect(root.querySelector('[role="alert"]')).toBeNull();
  });
});

function quiz(): StudentQuiz {
  return {
    id: 28,
    course_id: 4,
    title: 'Bài kiểm tra an toàn',
    duration_minutes: null,
    passing_score: '70',
    questions: [
      {
        id: 31,
        text: 'Quy tắc bảo mật',
        type: 'MULTIPLE_CHOICE',
        choices: [
          { id: 101, choice_text: 'Dùng mật khẩu riêng' },
          { id: 102, choice_text: 'Chia sẻ mật khẩu' },
        ],
      },
      {
        id: 32,
        text: 'Xác minh thông tin',
        type: 'MULTIPLE_CHOICE',
        choices: [{ id: 103, choice_text: 'Kiểm tra nguồn tin' }],
      },
    ],
  };
}

function attempt(answers: StudentQuizAnswer[] = []): StudentQuizAttempt {
  return {
    id: 501,
    quiz_id: 28,
    status: 'IN_PROGRESS',
    started_at: '2026-11-27T01:00:00Z',
    answers,
  };
}

function apiEnvelope<T>(data: T, businessCode: string) {
  return {
    success: true,
    businessCode,
    message: 'Quiz data loaded.',
    data,
    meta: {},
    traceId: 'st14-test',
  };
}
