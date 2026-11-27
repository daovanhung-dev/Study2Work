import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of, throwError } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import type { StudentLessonResources } from '../../shared/models/student-api.models';
import { ST12ResourcesService } from '../data-access/st12-resources.service';
import { ST12Page } from './st12-page';

@Component({ standalone: true, template: '<p>Resource route reached</p>' })
class ResourceRouteStub {}

describe('ST12Page', () => {
  let loadResources: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    loadResources = vi.fn(() => of(apiEnvelope(lesson())));

    await TestBed.configureTestingModule({
      imports: [ST12Page, ResourceRouteStub],
      providers: [
        provideRouter([
          { path: 'student/lessons/:lessonId/resources', component: ST12Page },
          { path: 'resources/:resourceId', component: ResourceRouteStub },
        ]),
        { provide: ST12ResourcesService, useValue: { resources: loadResources } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('loads the route lesson and renders API-backed resources', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/lessons/42/resources', ST12Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(loadResources).toHaveBeenCalledExactlyOnceWith('42');
    expect(root.querySelector('h1')?.textContent).toContain('Tài liệu kèm bài học');
    expect(root.textContent).toContain('Lesson resources');
    expect(root.textContent).toContain('Student handbook');
    expect(root.querySelector('.api-pill')?.textContent).toContain('1 tài liệu');
  });

  it('opens a resource through its ID and preserves the lesson return context', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/lessons/42/resources', ST12Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const link = root.querySelector<HTMLAnchorElement>('a.resource-open');
    expect(link?.getAttribute('href')).toBe('/resources/601?from=lesson&lessonId=42');
    link?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(TestBed.inject(Router).url).toBe('/resources/601?from=lesson&lessonId=42');
    expect(harness.routeNativeElement?.textContent).toContain('Resource route reached');
    expect(loadResources).toHaveBeenCalledExactlyOnceWith('42');
  });

  it('shows the empty state when #26 returns no resources', async () => {
    loadResources.mockReturnValueOnce(of(apiEnvelope({ ...lesson(), resources: [] })));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/lessons/42/resources', ST12Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Chưa có tài liệu được gắn với bài học này.');
    expect(root.querySelector('a.resource-open')).toBeNull();
    expect(root.textContent).toContain('Quay lại bài học');
  });

  it('offers retry and recovers after #26 fails', async () => {
    loadResources
      .mockReturnValueOnce(throwError(() => new Error('temporary failure')))
      .mockReturnValueOnce(of(apiEnvelope(lesson())));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/lessons/42/resources', ST12Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent?.trim()).toBeTruthy();
    expect(root.querySelector('button')?.textContent).toContain('Tải lại tài liệu');
    root.querySelector<HTMLButtonElement>('button')?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(loadResources).toHaveBeenCalledTimes(2);
    expect(loadResources).toHaveBeenNthCalledWith(1, '42');
    expect(loadResources).toHaveBeenNthCalledWith(2, '42');
    expect(root.textContent).toContain('Student handbook');
    expect(root.querySelector('[role="alert"]')).toBeNull();
  });

  it('does not expose a URL supplied outside the #26 resource projection', async () => {
    loadResources.mockReturnValueOnce(
      of(
        apiEnvelope({
          ...lesson(),
          resources: [
            {
              id: 601,
              name: 'Student handbook',
              type: 'PDF',
              url: 'https://files.example.test/handbook.pdf',
              lesson_id: 42,
            },
          ],
        }),
      ),
    );

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/lessons/42/resources', ST12Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Danh sách tài liệu chưa đúng định dạng.',
    );
    expect(root.querySelector('a.resource-open')).toBeNull();
    expect(root.textContent).not.toContain('files.example.test');
  });
});

function lesson(): StudentLessonResources {
  return {
    id: 42,
    course_id: 9,
    title: 'Lesson resources',
    content: null,
    video_url: null,
    order: 2,
    status: 'PUBLISHED',
    resources: [
      {
        id: 601,
        name: 'Student handbook',
        type: 'PDF',
        url: null,
        lesson_id: 42,
      },
    ],
  };
}

function apiEnvelope<T>(data: T) {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Lesson resources retrieved.',
    data,
    meta: {},
    traceId: 'st12-test',
  };
}
