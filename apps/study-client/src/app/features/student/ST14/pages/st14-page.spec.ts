import { TestBed } from '@angular/core/testing';
import type { ComponentFixture } from '@angular/core/testing';
import { ActivatedRoute, Router } from '@angular/router';
import { of } from 'rxjs';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudentApiService, type QuizAttemptRecord, type QuizRecord } from '../../data/student-api.service';
import { ST14Page } from './st14-page';

const quiz: QuizRecord = {
  id: 42,
  course_id: 7,
  title: 'Quiz',
  duration_minutes: 20,
  passing_score: '70',
  questions: [
    { id: 101, text: 'Question one', type: 'SINGLE_CHOICE', choices: [{ id: 201, text: 'Choice one' }] },
    { id: 102, text: 'Question two', type: 'SINGLE_CHOICE', choices: [{ id: 202, text: 'Choice two' }] },
    { id: 103, text: 'Question three', type: 'SINGLE_CHOICE', choices: [{ id: 203, text: 'Choice three' }] },
  ],
};

const attempt: QuizAttemptRecord = {
  id: 99,
  quiz_id: 42,
  status: 'IN_PROGRESS',
  started_at: '2026-11-17T00:00:00Z',
  answers: [],
};

function envelope<T>(data: T): ApiEnvelope<T> {
  return { success: true, businessCode: 'OK', message: '', data, meta: {}, traceId: 'test' };
}

describe('ST14Page question navigation', () => {
  let fixture: ComponentFixture<ST14Page>;
  let getQuiz: ReturnType<typeof vi.fn>;
  let saveAnswer: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    getQuiz = vi.fn().mockReturnValue(of(envelope(quiz)));
    saveAnswer = vi.fn().mockReturnValue(of(envelope(attempt)));

    await TestBed.configureTestingModule({
      imports: [ST14Page],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: { get: (key: string) => (key === 'quizId' ? '42' : key === 'attemptId' ? '99' : null) },
            },
          },
        },
        { provide: Router, useValue: { navigate: vi.fn() } },
        { provide: StudentApiService, useValue: { getQuiz, saveAnswer } },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(ST14Page);
    fixture.detectChanges();
  });

  it('moves by the API question order and keeps navigation local', () => {
    const root = fixture.nativeElement as HTMLElement;
    const questionText = () => root.querySelector('.question-panel h2')?.textContent?.trim();
    const previous = root.querySelector<HTMLButtonElement>('[data-action="previous-question"]')!;
    const next = root.querySelector<HTMLButtonElement>('[data-action="next-question"]')!;

    expect(questionText()).toBe('Question one');
    expect(previous.disabled).toBe(true);
    expect(next.disabled).toBe(false);

    next.click();
    fixture.detectChanges();
    expect(questionText()).toBe('Question two');

    root.querySelector<HTMLButtonElement>('[data-question-index="2"]')!.click();
    fixture.detectChanges();
    expect(questionText()).toBe('Question three');
    expect(next.disabled).toBe(true);

    root.querySelector<HTMLButtonElement>('[data-question-index="0"]')!.click();
    fixture.detectChanges();
    expect(questionText()).toBe('Question one');
    expect(getQuiz).toHaveBeenCalledTimes(1);
    expect(saveAnswer).not.toHaveBeenCalled();
  });

  it('preserves a selected choice when leaving and returning to its question', () => {
    const root = fixture.nativeElement as HTMLElement;
    const firstChoice = root.querySelector<HTMLInputElement>('.question-panel input[type="checkbox"]')!;
    firstChoice.click();
    fixture.detectChanges();

    expect(saveAnswer).toHaveBeenCalledWith('99', 101, [201]);

    root.querySelector<HTMLButtonElement>('[data-action="next-question"]')!.click();
    fixture.detectChanges();
    root.querySelector<HTMLButtonElement>('[data-question-index="0"]')!.click();
    fixture.detectChanges();

    expect(root.querySelector<HTMLInputElement>('.question-panel input[type="checkbox"]')?.checked).toBe(true);
  });
});
