import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ST24CreateDiscussionService } from '../data-access/st24-create-discussion.service';
import type {
  StudentCourseSummary,
  StudentDiscussion,
  StudentPage,
} from '../../shared/models/student-api.models';
import { ST24Page } from './st24-page';

@Component({ standalone: true, template: '' })
class DiscussionListRouteStub {}

describe('ST24Page', () => {
  let courses: ReturnType<typeof vi.fn>;
  let create: ReturnType<typeof vi.fn>;
  let refresh: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    courses = vi.fn(() => of(apiEnvelope(coursePage(), 'DESIGN_RESOURCE_RETRIEVED')));
    create = vi.fn((courseId: number, title: string, content: string) =>
      of(apiEnvelope(createdDiscussionPage(courseId, title, content), 'DESIGN_RESOURCE_CREATED')),
    );
    refresh = vi.fn((courseId: number, title = 'A question', content = 'Some details') =>
      of(apiEnvelope(discussionListPage(courseId, title, content), 'DESIGN_RESOURCE_RETRIEVED')),
    );

    await TestBed.configureTestingModule({
      imports: [ST24Page, DiscussionListRouteStub],
      providers: [
        provideRouter([
          { path: 'student/discussions/new', component: ST24Page },
          { path: 'student/discussions', component: DiscussionListRouteStub },
        ]),
        { provide: ST24CreateDiscussionService, useValue: { courses, create, refresh } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('keeps the create request gated while required form fields are blank', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/student/discussions/new', ST24Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const course = root.querySelector<HTMLSelectElement>('select[name="courseId"]');
    expect(course).not.toBeNull();
    if (course) {
      course.value = '12';
      course.dispatchEvent(new Event('change', { bubbles: true }));
    }
    harness.fixture.detectChanges();

    const form = root.querySelector<HTMLFormElement>('form');
    expect(page.selectedCourseId()).toBe('12');
    expect(form?.checkValidity()).toBe(false);
    root.querySelector<HTMLButtonElement>('button[type="submit"]')?.click();
    await harness.fixture.whenStable();

    expect(create).not.toHaveBeenCalled();
    expect(page.creationAccepted()).toBe(false);
  });

  it('confirms a valid creation only after the #39 course refresh contains the new discussion', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/student/discussions/new', ST24Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const course = root.querySelector<HTMLSelectElement>('select[name="courseId"]');
    const title = root.querySelector<HTMLInputElement>('input[name="title"]');
    const content = root.querySelector<HTMLTextAreaElement>('textarea[name="content"]');
    expect(course && title && content).not.toBeNull();

    if (course) {
      course.value = '12';
      course.dispatchEvent(new Event('change', { bubbles: true }));
    }
    if (title) {
      title.value = '  A question  ';
      title.dispatchEvent(new Event('input', { bubbles: true }));
    }
    if (content) {
      content.value = '  Some details  ';
      content.dispatchEvent(new Event('input', { bubbles: true }));
    }
    harness.fixture.detectChanges();
    root.querySelector<HTMLButtonElement>('button[type="submit"]')?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(create).toHaveBeenCalledExactlyOnceWith(12, 'A question', 'Some details');
    expect(page.creationAccepted()).toBe(true);
    expect(page.createdId()).toBe('91');
    expect(refresh).toHaveBeenCalledExactlyOnceWith(12);
    expect(TestBed.inject(Router).url).toBe('/student/discussions?courseId=12');
  });
});

function coursePage(): StudentPage<StudentCourseSummary> {
  return {
    items: [
      {
        course_id: 12,
        name: 'Active course',
        enrollment_status: 'ACTIVE',
        enrolled_at: '2026-11-26T09:00:00Z',
      },
    ],
    pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
  };
}

function createdDiscussionPage(
  courseId: number,
  title: string,
  content: string,
): StudentPage<StudentDiscussion> {
  return {
    items: [
      {
        id: 91,
        course_id: courseId,
        title,
        content,
        author: { id: 7, full_name: 'Student', avatar_url: null },
        status: 'ACTIVE',
        comments: [],
      },
    ],
    pagination: { page: 1, size: 1, total: 1, total_pages: 1 },
  };
}

function discussionListPage(
  courseId: number,
  title: string,
  content: string,
): StudentPage<StudentDiscussion> {
  return {
    items: [
      {
        id: 91,
        course_id: courseId,
        title,
        content,
        author: { id: 7, full_name: 'Student', avatar_url: null },
        status: 'ACTIVE',
        comments: [],
      },
    ],
    pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
  };
}

function apiEnvelope<T>(data: T, businessCode: string) {
  return {
    success: true,
    businessCode,
    message: 'Discussion data loaded.',
    data,
    meta: {},
    traceId: 'st24-test',
  };
}
