import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { MentorSessionService } from '../../../../core/auth/mentor-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type {
  MentorCourse,
  MentorLecture,
  MentorPage,
  MentorUploadAsset,
} from '../../shared/models/mentor-api.models';
import { blockME04DepartureDuringWrite, ME04Page } from './me04-page';

@Component({ standalone: true, template: '<p>Lecture destination</p>' })
class LectureDestinationStub {}

describe('ME04Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ME04Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([
          {
            path: 'mentor/courses/:courseId/lectures/new',
            component: ME04Page,
            canDeactivate: [blockME04DepartureDuringWrite],
          },
          { path: 'mentor/lectures/:lectureId', component: LectureDestinationStub },
        ]),
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('loads authenticated #46 and maps #34 upload into #47 create before opening ME-05', async () => {
    const { harness, page } = await openLoadedPage();
    const root = harness.routeNativeElement!;

    expect(page.loading()).toBe(false);
    expect(root.textContent).toContain('English Basics');
    expect(root.textContent).toContain('Tệp đính kèm');

    const file = new File(['lecture notes'], 'notes.pdf', { type: 'application/pdf' });
    selectFile(root, file);
    harness.fixture.detectChanges();
    const uploadButton = findButton(root, 'Tải lên');
    uploadButton.click();
    harness.fixture.detectChanges();

    const uploadRequest = http.expectOne('/api/v1/uploads');
    expect(uploadRequest.request.method).toBe('POST');
    expect(uploadRequest.request.headers.get('Authorization')).toBe('Bearer mentor-access-token');
    const uploadBody = uploadRequest.request.body as FormData;
    expect(uploadBody.get('purpose')).toBe('LECTURE');
    expect(uploadBody.get('course_id')).toBe('7');
    expect((uploadBody.get('file') as File).name).toBe('notes.pdf');
    uploadRequest.flush(successEnvelope(uploadAsset(81), 'DESIGN_RESOURCE_CREATED'));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(page.selectedFiles()[0]?.asset?.id).toBe(81);
    expect(root.textContent).toContain('Đã tải lên · Asset #81');

    setValue(root, '#me04-title', 'Lesson One');
    setValue(root, '#me04-content', '# Welcome\nRead these notes.');
    setValue(root, '#me04-order', '3');
    harness.fixture.detectChanges();

    const createButton = root.querySelector<HTMLButtonElement>('button[type="submit"]');
    if (!createButton) throw new Error('ME-04 create button is missing.');
    expect(createButton.disabled).toBe(false);
    createButton.click();
    harness.fixture.detectChanges();

    const createRequest = http.expectOne('/api/v1/mentor/courses/7/lectures');
    expect(createRequest.request.method).toBe('POST');
    expect(createRequest.request.headers.get('Authorization')).toBe('Bearer mentor-access-token');
    expect(createRequest.request.params.keys()).toEqual([]);
    expect(createRequest.request.body).toEqual({
      title: 'Lesson One',
      content: '# Welcome\nRead these notes.',
      asset_refs: '[81]',
      order: 3,
    });
    createRequest.flush(successEnvelope(lecture(90, 81), 'DESIGN_RESOURCE_CREATED'));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(TestBed.inject(Router).url).toBe('/mentor/lectures/90');
    expect(harness.routeNativeElement?.textContent).toContain('Lecture destination');
  });

  it('rejects an invalid course route ID without issuing an API request', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/mentor/courses/not-an-id/lectures/new', ME04Page);
    harness.fixture.detectChanges();

    expect(page.invalidId()).toBe(true);
    expect(harness.routeNativeElement?.querySelector('[role="alert"]')?.textContent).toContain(
      'Course ID trên đường dẫn không phải số nguyên dương int64.',
    );
    http.expectNone('/api/v1/mentor/courses');
    http.expectNone('/api/v1/uploads');
    http.expectNone('/api/v1/mentor/courses/not-an-id/lectures');
  });

  it('shows a #46 load failure and retries the course request on demand', async () => {
    signInAsMentor();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/mentor/courses/7/lectures/new', ME04Page);
    const initialRequest = http.expectOne(
      (candidate) => candidate.url === '/api/v1/mentor/courses',
    );
    initialRequest.flush(
      {
        success: false,
        businessCode: 'DESIGN_INTERNAL_ERROR',
        message: 'Course list unavailable.',
        data: null,
        meta: {},
        traceId: 'me04-courses-error',
      },
      { status: 503, statusText: 'Service Unavailable' },
    );
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(page.error()).toContain('Course list unavailable.');
    const root = harness.routeNativeElement!;
    expect(root.querySelector('[role="alert"]')?.textContent).toContain('Course list unavailable.');
    findButton(root, 'Tải lại').click();
    harness.fixture.detectChanges();

    const retryRequest = http.expectOne((candidate) => candidate.url === '/api/v1/mentor/courses');
    expect(retryRequest.request.method).toBe('GET');
    expect(retryRequest.request.headers.get('Authorization')).toBe('Bearer mentor-access-token');
    expect(retryRequest.request.params.get('page')).toBe('1');
    expect(retryRequest.request.params.get('size')).toBe('100');
    retryRequest.flush(successEnvelope(coursePage([course()], 1, 100, 1)));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(page.error()).toBeNull();
    expect(root.textContent).toContain('English Basics');
  });

  it('blocks #47 until every selected file has a confirmed upload', async () => {
    const { harness, page } = await openLoadedPage();
    const root = harness.routeNativeElement!;
    const file = new File(['lecture notes'], 'notes.pdf', { type: 'application/pdf' });
    selectFile(root, file);
    harness.fixture.detectChanges();
    findButton(root, 'Tải lên').click();
    harness.fixture.detectChanges();

    const uploadRequest = http.expectOne('/api/v1/uploads');
    uploadRequest.error(new ProgressEvent('error'));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    setValue(root, '#me04-title', 'Lesson One');
    setValue(root, '#me04-content', 'Lesson content.');
    harness.fixture.detectChanges();
    const createButton = root.querySelector<HTMLButtonElement>('button[type="submit"]');
    if (!createButton) throw new Error('ME-04 create button is missing.');
    createButton.click();
    harness.fixture.detectChanges();

    expect(page.selectedFiles()[0]?.retryBlocked).toBe(true);
    expect(root.textContent).toContain('Kết quả chưa xác định; không tự gửi lại');
    expect(root.querySelector('.me04-file-list button')?.textContent?.trim()).toBe('Bỏ khỏi danh sách');
    expect(page.formError()).toContain('Tải lên hoặc bỏ khỏi danh sách');
    http.expectNone('/api/v1/uploads');
    http.expectNone('/api/v1/mentor/courses/7/lectures');
  });

  it('locks the submit action after an ambiguous #47 result to prevent duplicate lectures', async () => {
    const { harness, page } = await openLoadedPage();
    const root = harness.routeNativeElement!;
    setValue(root, '#me04-title', 'Lesson One');
    setValue(root, '#me04-content', 'Lesson content.');
    harness.fixture.detectChanges();

    const createButton = root.querySelector<HTMLButtonElement>('button[type="submit"]');
    if (!createButton) throw new Error('ME-04 create button is missing.');
    expect(createButton.disabled).toBe(false);
    createButton.click();
    harness.fixture.detectChanges();

    const request = http.expectOne('/api/v1/mentor/courses/7/lectures');
    expect(request.request.body).toEqual({
      title: 'Lesson One',
      content: 'Lesson content.',
      asset_refs: '[]',
      order: 0,
    });
    request.error(new ProgressEvent('error'));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(page.createOutcomeUnknown()).toBe(true);
    expect(createButton.disabled).toBe(true);
    expect(root.textContent).toContain('Không gửi lại yêu cầu để tránh tạo lecture trùng.');
    createButton.click();
    http.expectNone('/api/v1/mentor/courses/7/lectures');
  });

  async function openLoadedPage() {
    signInAsMentor();
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/mentor/courses/7/lectures/new', ME04Page);
    expect(page.loading()).toBe(true);
    expect(harness.routeNativeElement?.querySelector('[role="status"]')?.textContent).toContain(
      'Đang tải khóa học',
    );

    const request = http.expectOne((candidate) => candidate.url === '/api/v1/mentor/courses');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer mentor-access-token');
    expect(request.request.params.keys().sort()).toEqual(['page', 'size']);
    expect(request.request.params.get('page')).toBe('1');
    expect(request.request.params.get('size')).toBe('100');
    expect(request.request.body).toBeNull();
    request.flush(successEnvelope(coursePage([course()], 1, 100, 1)));
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();
    return { harness, page };
  }

  function signInAsMentor(): void {
    TestBed.inject(MentorSessionService).acceptLoginEnvelope(
      successEnvelope({
        full_name: 'Mentor One',
        email: 'mentor@example.test',
        role: 'MENTOR',
        access_token: 'mentor-access-token',
        refresh_token: 'mentor-refresh-token',
        token_type: 'bearer',
        expires_in: 3600,
        refresh_expires_in: 7200,
      }),
    );
  }
});

function findButton(root: HTMLElement, label: string): HTMLButtonElement {
  const button = Array.from(root.querySelectorAll<HTMLButtonElement>('button')).find(
    (candidate) => candidate.textContent?.trim() === label,
  );
  if (!button) throw new Error(`ME-04 button “${label}” is missing.`);
  return button;
}

function selectFile(root: HTMLElement, file: File): void {
  const input = root.querySelector<HTMLInputElement>('#me04-files');
  if (!input) throw new Error('ME-04 file input is missing.');
  Object.defineProperty(input, 'files', { configurable: true, value: [file] });
  input.dispatchEvent(new Event('change', { bubbles: true }));
}

function setValue(root: HTMLElement, selector: string, value: string): void {
  const input = root.querySelector<HTMLInputElement | HTMLTextAreaElement>(selector);
  if (!input) throw new Error(`ME-04 field “${selector}” is missing.`);
  input.value = value;
  input.dispatchEvent(new Event('input', { bubbles: true }));
  input.dispatchEvent(new Event('change', { bubbles: true }));
}

function successEnvelope<T>(
  data: T,
  businessCode = 'DESIGN_RESOURCE_RETRIEVED',
): ApiEnvelope<T> {
  return {
    success: true,
    businessCode,
    message: 'ok',
    data,
    meta: {},
    traceId: 'me04-test',
  };
}

function coursePage(
  items: MentorCourse[],
  page: number,
  size: number,
  total: number,
): MentorPage<MentorCourse> {
  return {
    items,
    pagination: {
      page,
      size,
      total,
      total_pages: total === 0 ? 0 : Math.ceil(total / size),
    },
  };
}

function course(): MentorCourse {
  return {
    id: 7,
    title: 'English Basics',
    description: 'Course description.',
    thumbnail_url: null,
    price: '10.00',
    status: 'PUBLISHED',
    mentor: { id: 5, full_name: 'Mentor One', avatar_url: null },
  };
}

function uploadAsset(id: number): MentorUploadAsset {
  return {
    id,
    name: 'notes.pdf',
    url: 'https://storage.example.test/notes.pdf',
    content_type: 'application/pdf',
    size_bytes: 13,
    status: 'UPLOADED',
  };
}

function lecture(id: number, assetId: number): MentorLecture {
  return {
    id,
    course_id: 7,
    title: 'Lesson One',
    content: '# Welcome\nRead these notes.',
    assets: [uploadAsset(assetId)],
    order: 3,
    status: 'PUBLISHED',
  };
}
