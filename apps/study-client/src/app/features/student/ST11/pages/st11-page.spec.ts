import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of, throwError } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import type { StudentLesson } from '../../shared/models/student-api.models';
import { ST11LessonService } from '../data-access/st11-lesson.service';
import { ST11Page } from './st11-page';

@Component({ standalone: true, template: '<p>Lesson resources route reached</p>' })
class LessonResourcesRouteStub {}

describe('ST11Page', () => {
  let loadLesson: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    loadLesson = vi.fn(() => of(apiEnvelope(lesson())));

    await TestBed.configureTestingModule({
      imports: [ST11Page, LessonResourcesRouteStub],
      providers: [
        provideRouter([
          { path: 'student/lessons/:lessonId', component: ST11Page },
          { path: 'student/lessons/:lessonId/resources', component: LessonResourcesRouteStub },
        ]),
        { provide: ST11LessonService, useValue: { lesson: loadLesson } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('loads API #24 content and keeps the unavailable player and progress actions gated', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/lessons/42', ST11Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(loadLesson).toHaveBeenCalledExactlyOnceWith('42');
    expect(root.querySelector('h1')?.textContent).toContain('Bài học an toàn');
    expect(root.textContent).toContain('Nội dung hướng dẫn an toàn.');
    expect(root.querySelector('.api-pill')?.textContent).toContain('Đã xuất bản');
    expect(root.textContent).toContain('Video bài học hiện chưa khả dụng');
    expect(root.textContent).toContain('Bài học sẽ không được tự đánh dấu hoàn thành.');
    expect(root.querySelector('video, iframe, audio, button')).toBeNull();
    expect(root.textContent).not.toContain('media.example.test');
    expect(root.querySelector<HTMLAnchorElement>('.api-actions a')?.getAttribute('href')).toBe(
      '/student/lessons/42/resources',
    );
  });

  it('does not call #24 for an invalid route lesson ID', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/lessons/not-a-number', ST11Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(loadLesson).not.toHaveBeenCalled();
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Không tìm thấy bài học này.',
    );
    expect(root.querySelector('button')?.textContent).toContain('Tải lại bài học');
  });

  it('rejects a successful #24 envelope with an unsupported business code', async () => {
    loadLesson.mockReturnValueOnce(of(apiEnvelope(lesson(), 'LESSON_NOT_READY')));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/lessons/42', ST11Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Chưa thể tải nội dung bài học.',
    );
    expect(root.textContent).not.toContain('Nội dung hướng dẫn an toàn.');
  });

  it('rejects a #24 payload whose lesson ID does not match the route', async () => {
    loadLesson.mockReturnValueOnce(of(apiEnvelope({ ...lesson(), id: 99 })));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/lessons/42', ST11Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Không tìm thấy bài học này.',
    );
    expect(root.textContent).not.toContain('Bài học an toàn');
  });

  it('offers retry and recovers after #24 fails', async () => {
    loadLesson
      .mockReturnValueOnce(throwError(() => new Error('temporary failure')))
      .mockReturnValueOnce(of(apiEnvelope(lesson())));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/lessons/42', ST11Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent?.trim()).toBeTruthy();
    root.querySelector<HTMLButtonElement>('button')?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(loadLesson).toHaveBeenCalledTimes(2);
    expect(loadLesson).toHaveBeenNthCalledWith(1, '42');
    expect(loadLesson).toHaveBeenNthCalledWith(2, '42');
    expect(root.textContent).toContain('Nội dung hướng dẫn an toàn.');
    expect(root.querySelector('[role="alert"]')).toBeNull();
  });
});

function lesson(): StudentLesson {
  return {
    id: 42,
    course_id: 9,
    title: 'Bài học an toàn',
    content: 'Nội dung hướng dẫn an toàn.',
    video_url: 'https://media.example.test/lesson.mp4',
    order: 2,
    status: 'PUBLISHED',
  };
}

function apiEnvelope<T>(data: T, businessCode = 'DESIGN_RESOURCE_RETRIEVED') {
  return {
    success: true,
    businessCode,
    message: 'Lesson loaded.',
    data,
    meta: {},
    traceId: 'st11-test',
  };
}
