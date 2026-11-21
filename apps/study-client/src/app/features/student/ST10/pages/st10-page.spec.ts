import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import type { StudentLesson } from '../../shared/models/student-api.models';
import { ST10Page } from './st10-page';

@Component({ template: '<main data-screen-id="ST-11">ST-11 destination</main>' })
class ST11DestinationStub {}

describe('ST10Page', () => {
  let apiRequest: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    apiRequest = vi.fn();
    apiRequest.mockReturnValue(of(apiEnvelope(lesson(), 'DESIGN_RESOURCE_RETRIEVED')));

    await TestBed.configureTestingModule({
      imports: [ST10Page, ST11DestinationStub],
      providers: [
        provideRouter([
          { path: 'student/lessons/:lessonId/start', component: ST10Page },
          { path: 'student/lessons/:lessonId', component: ST11DestinationStub },
        ]),
        { provide: StudentApiService, useValue: { request: apiRequest } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('checks access on entry and starts only after an explicit click', async () => {
    apiRequest
      .mockReturnValueOnce(of(apiEnvelope(lesson(), 'DESIGN_RESOURCE_RETRIEVED')))
      .mockReturnValueOnce(of(apiEnvelope(lesson(), 'DESIGN_RESOURCE_CREATED')));
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/lessons/42/start', ST10Page);

    expect(apiRequest).toHaveBeenCalledTimes(1);
    expect(apiRequest).toHaveBeenNthCalledWith(1, STUDY_SERVER_APIS.API_022, {
      pathParams: { lesson_id: '42' },
    });

    const root = harness.routeNativeElement as HTMLElement;
    const startButton = findStartButton(root);
    expect(startButton.disabled).toBe(false);
    expect(apiRequest).toHaveBeenCalledTimes(1);
    expect(root.textContent).not.toContain('protected lesson body');
    expect(root.textContent).not.toContain('https://media.example/lesson.mp4');
    expect(root.querySelector('video')).toBeNull();

    startButton.click();
    harness.fixture.detectChanges();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(apiRequest).toHaveBeenNthCalledWith(2, STUDY_SERVER_APIS.API_023, {
      pathParams: { lesson_id: '42' },
    });
    expect(TestBed.inject(Router).url).toBe('/student/lessons/42');
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain('ST-11 destination');
  });

  it('keeps start disabled when access returns a non-published lesson', async () => {
    apiRequest.mockReturnValue(
      of(apiEnvelope(lesson({ status: 'DRAFT' }), 'DESIGN_RESOURCE_RETRIEVED')),
    );

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/lessons/42/start', ST10Page);

    const root = harness.routeNativeElement as HTMLElement;
    const startButton = findStartButton(root);
    expect(startButton.disabled).toBe(true);
    startButton.click();
    harness.fixture.detectChanges();

    expect(apiRequest).toHaveBeenCalledTimes(1);
    expect(apiRequest).toHaveBeenCalledWith(STUDY_SERVER_APIS.API_022, {
      pathParams: { lesson_id: '42' },
    });
    expect(TestBed.inject(Router).url).toBe('/student/lessons/42/start');
  });

  it('does not hand off when start responds for a different lesson', async () => {
    apiRequest
      .mockReturnValueOnce(of(apiEnvelope(lesson(), 'DESIGN_RESOURCE_RETRIEVED')))
      .mockReturnValueOnce(of(apiEnvelope(lesson({ id: 99 }), 'DESIGN_RESOURCE_CREATED')));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/lessons/42/start', ST10Page);
    findStartButton(harness.routeNativeElement as HTMLElement).click();
    harness.fixture.detectChanges();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(TestBed.inject(Router).url).toBe('/student/lessons/42/start');
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain(
      'Bài học chưa sẵn sàng để bắt đầu.',
    );
  });
});

function findStartButton(root: HTMLElement): HTMLButtonElement {
  const button = Array.from(root.querySelectorAll('button')).find((candidate) =>
    candidate.textContent?.includes('Bắt đầu học'),
  );
  if (!(button instanceof HTMLButtonElement)) throw new Error('ST-10 start button is missing.');
  return button;
}

function lesson(overrides: Partial<StudentLesson> = {}): StudentLesson {
  return {
    id: 42,
    course_id: 7,
    title: 'Lesson preview',
    content: 'protected lesson body',
    video_url: 'https://media.example/lesson.mp4',
    order: 1,
    status: 'PUBLISHED',
    ...overrides,
  };
}

function apiEnvelope(data: StudentLesson, businessCode: string) {
  return {
    success: true,
    businessCode,
    message: 'Lesson retrieved.',
    data,
    meta: {},
    traceId: 'st10-test',
  };
}
