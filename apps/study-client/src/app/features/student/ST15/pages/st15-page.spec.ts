import { HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { Subject, of, throwError } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ST15SubmitService } from '../data-access/st15-submit.service';
import { ST15Page } from './st15-page';

@Component({ template: '<main data-screen-id="ST-16">ST-16 destination</main>' })
class ST16DestinationStub {}

describe('ST15Page', () => {
  let submitAttempt: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    submitAttempt = vi.fn();

    await TestBed.configureTestingModule({
      imports: [ST15Page, ST16DestinationStub],
      providers: [
        provideRouter([
          { path: 'student/attempts/:attemptId/submit', component: ST15Page },
          { path: 'student/attempts/:attemptId/result', component: ST16DestinationStub },
        ]),
        { provide: ST15SubmitService, useValue: { submit: submitAttempt } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('submits only after confirmation and opens the result after an accepted response', async () => {
    submitAttempt.mockReturnValue(of(apiEnvelope(submittedAttempt(42))));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/attempts/42/submit', ST15Page);

    expect(submitAttempt).not.toHaveBeenCalled();

    const root = harness.routeNativeElement as HTMLElement;
    findSubmitButton(root).click();
    harness.fixture.detectChanges();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(submitAttempt).toHaveBeenCalledTimes(1);
    expect(submitAttempt).toHaveBeenCalledWith('42');
    expect(TestBed.inject(Router).url).toBe('/student/attempts/42/result');
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain('ST-16 destination');
  });

  it('ignores a second activation while the submit request is pending', async () => {
    const pending = new Subject<unknown>();
    submitAttempt.mockReturnValue(pending);

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/attempts/42/submit', ST15Page);

    const root = harness.routeNativeElement as HTMLElement;
    const submitButton = findSubmitButton(root);
    submitButton.click();
    harness.fixture.detectChanges();

    expect(submitAttempt).toHaveBeenCalledTimes(1);
    expect(submitAttempt).toHaveBeenCalledWith('42');
    expect(submitButton.disabled).toBe(true);

    submitButton.click();
    expect(submitAttempt).toHaveBeenCalledTimes(1);

    pending.complete();
  });

  it('blocks a blind repeat and stays on the submit page after a network error', async () => {
    submitAttempt.mockReturnValue(
      throwError(() => new HttpErrorResponse({ status: 0, statusText: 'Unknown Error' })),
    );

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/attempts/42/submit', ST15Page);

    const root = harness.routeNativeElement as HTMLElement;
    const submitButton = findSubmitButton(root);
    submitButton.click();
    harness.fixture.detectChanges();

    expect(submitAttempt).toHaveBeenCalledTimes(1);
    expect(submitButton.disabled).toBe(true);
    expect(TestBed.inject(Router).url).toBe('/student/attempts/42/submit');

    submitButton.click();
    expect(submitAttempt).toHaveBeenCalledTimes(1);
  });

  it('does not treat a closed-attempt conflict as accepted or allow another submit', async () => {
    submitAttempt.mockReturnValue(
      throwError(() => new HttpErrorResponse({ status: 409, statusText: 'Conflict' })),
    );

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/attempts/42/submit', ST15Page);

    const root = harness.routeNativeElement as HTMLElement;
    const submitButton = findSubmitButton(root);
    submitButton.click();
    harness.fixture.detectChanges();

    expect(submitAttempt).toHaveBeenCalledTimes(1);
    expect(submitButton.disabled).toBe(true);
    expect(TestBed.inject(Router).url).toBe('/student/attempts/42/submit');
  });
});

function findSubmitButton(root: HTMLElement): HTMLButtonElement {
  const button = root.querySelector('button.api-button:not(.secondary)');
  if (!(button instanceof HTMLButtonElement)) throw new Error('ST-15 submit button is missing.');
  return button;
}

function submittedAttempt(id: number) {
  return {
    id,
    quiz_id: 7,
    status: 'GRADED',
    started_at: '2026-11-27T03:00:00Z',
    submitted_at: '2026-11-27T03:05:00Z',
    score: 100,
    passed: true,
    answers: [],
  };
}

function apiEnvelope(data: ReturnType<typeof submittedAttempt>) {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_UPDATED',
    message: 'Attempt submitted.',
    data,
    meta: {},
    traceId: 'st15-test',
  };
}
