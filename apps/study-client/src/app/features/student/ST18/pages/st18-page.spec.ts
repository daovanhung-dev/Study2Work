import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { Subject, of, throwError } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ST18SubmissionService } from '../data-access/st18-submission.service';
import { ST18Page } from './st18-page';

describe('ST18Page', () => {
  let assignment: ReturnType<typeof vi.fn>;
  let upload: ReturnType<typeof vi.fn>;
  let submit: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    assignment = vi.fn().mockReturnValue(of(apiEnvelope(assignmentData())));
    upload = vi.fn();
    submit = vi.fn();

    await TestBed.configureTestingModule({
      imports: [ST18Page],
      providers: [
        provideRouter([{ path: 'student/assignments/:assignmentId/submit', component: ST18Page }]),
        { provide: ST18SubmissionService, useValue: { assignment, upload, submit } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('shows one local alert when the submission outcome is unknown', async () => {
    submit.mockReturnValue(
      throwError(() => new HttpErrorResponse({ status: 0, statusText: 'Unknown Error' })),
    );

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/assignments/42/submit', ST18Page);
    const root = harness.routeNativeElement as HTMLElement;
    enterSubmissionText(root, harness);
    findSubmitButton(root).click();
    harness.fixture.detectChanges();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(submit).toHaveBeenCalledTimes(1);
    expect(upload).not.toHaveBeenCalled();
    expectSingleInFormAlert(
      root,
      'Chưa thể xác nhận bài đã được gửi. Nút gửi đã khóa để tránh gửi trùng.',
    );
  });

  it('keeps an uncertain upload message distinct from submission status', async () => {
    upload.mockReturnValue(
      throwError(() => new HttpErrorResponse({ status: 0, statusText: 'Unknown Error' })),
    );

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/assignments/42/submit', ST18Page);
    const root = harness.routeNativeElement as HTMLElement;
    selectFile(root);
    findSubmitButton(root).click();
    harness.fixture.detectChanges();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(upload).toHaveBeenCalledTimes(1);
    expect(submit).not.toHaveBeenCalled();
    expectSingleInFormAlert(root, 'Upload chưa trả về xác nhận hợp lệ; không gửi lại để tránh tải trùng.');
    expect(root.textContent).not.toContain('Chưa thể xác nhận bài đã được gửi.');
  });

  it('labels the submit action as uploading while the upload request is pending', async () => {
    const pendingUpload = new Subject<unknown>();
    upload.mockReturnValue(pendingUpload);

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/assignments/42/submit', ST18Page);
    const root = harness.routeNativeElement as HTMLElement;
    selectFile(root);
    findSubmitButton(root).click();
    harness.fixture.detectChanges();

    expect(upload).toHaveBeenCalledTimes(1);
    expect(submit).not.toHaveBeenCalled();
    expect(findSubmitButton(root).textContent).toContain('Đang tải tệp…');
    expect(findSubmitButton(root).textContent).not.toContain('Đang gửi bài…');

    pendingUpload.complete();
  });

  it('labels a text-only in-flight request as submitting', async () => {
    const pendingSubmission = new Subject<unknown>();
    submit.mockReturnValue(pendingSubmission);

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/assignments/42/submit', ST18Page);
    const root = harness.routeNativeElement as HTMLElement;
    enterSubmissionText(root, harness);
    findSubmitButton(root).click();
    harness.fixture.detectChanges();

    expect(upload).not.toHaveBeenCalled();
    expect(submit).toHaveBeenCalledWith('42', 'My submission', null);
    expect(findSubmitButton(root).textContent).toContain('Đang gửi bài…');
    expect(findSubmitButton(root).textContent).not.toContain('Đang tải tệp…');

    pendingSubmission.complete();
  });

  it('announces upload completion while the final submission is pending', async () => {
    upload.mockReturnValue(of(apiEnvelope(uploadData(), 'DESIGN_RESOURCE_CREATED')));
    const pendingSubmission = new Subject<unknown>();
    submit.mockReturnValue(pendingSubmission);

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/assignments/42/submit', ST18Page);
    const root = harness.routeNativeElement as HTMLElement;
    selectFile(root);
    findSubmitButton(root).click();
    harness.fixture.detectChanges();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const uploadStatus = root.querySelector('.api-success[role="status"]');
    expect(upload).toHaveBeenCalledTimes(1);
    expect(submit).toHaveBeenCalledWith('42', null, 77);
    expect(uploadStatus?.textContent).toContain('Đã tải tệp submission.txt lên. Đang gửi bài.');
    expect(uploadStatus?.textContent).not.toContain('Bấm nộp để gửi bài.');
    expect(root.textContent).not.toContain('Bài nộp đã được tạo.');
    expect(findSubmitButton(root).disabled).toBe(true);
    expect(findSubmitButton(root).textContent).toContain('Đang gửi bài…');

    pendingSubmission.complete();
  });

  it('keeps upload success distinct when final submission outcome is unknown', async () => {
    upload.mockReturnValue(of(apiEnvelope(uploadData(), 'DESIGN_RESOURCE_CREATED')));
    submit.mockReturnValue(
      throwError(() => new HttpErrorResponse({ status: 0, statusText: 'Unknown Error' })),
    );

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/assignments/42/submit', ST18Page);
    const root = harness.routeNativeElement as HTMLElement;
    selectFile(root);
    findSubmitButton(root).click();
    harness.fixture.detectChanges();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const uploadStatus = root.querySelector('.api-success[role="status"]');
    expect(uploadStatus?.textContent?.trim()).toBe('Đã tải tệp submission.txt lên.');
    expect(uploadStatus?.textContent).not.toContain('Bấm nộp để gửi bài.');
    expectSingleInFormAlert(
      root,
      'Chưa thể xác nhận bài đã được gửi. Nút gửi đã khóa để tránh gửi trùng.',
    );
    expect(findSubmitButton(root).disabled).toBe(true);
  });
});

function enterSubmissionText(root: HTMLElement, harness: RouterTestingHarness): void {
  const textarea = root.querySelector('textarea[name="content"]');
  if (!(textarea instanceof HTMLTextAreaElement)) throw new Error('ST-18 content field is missing.');
  textarea.value = 'My submission';
  textarea.dispatchEvent(new Event('input', { bubbles: true }));
  harness.fixture.detectChanges();
}

function selectFile(root: HTMLElement): void {
  const input = root.querySelector('input[type="file"]');
  if (!(input instanceof HTMLInputElement)) throw new Error('ST-18 file field is missing.');
  Object.defineProperty(input, 'files', {
    configurable: true,
    value: [new File(['submission'], 'submission.txt', { type: 'text/plain' })],
  });
  input.dispatchEvent(new Event('change', { bubbles: true }));
}

function findSubmitButton(root: HTMLElement): HTMLButtonElement {
  const button = root.querySelector('button[type="submit"]');
  if (!(button instanceof HTMLButtonElement)) throw new Error('ST-18 submit button is missing.');
  return button;
}

function expectSingleInFormAlert(root: HTMLElement, message: string): void {
  const alerts = root.querySelectorAll('[role="alert"]');
  expect(alerts).toHaveLength(1);
  expect(alerts[0].tagName).toBe('P');
  expect(alerts[0].closest('form')).not.toBeNull();
  expect(alerts[0].textContent).toContain(message);
  expect(root.querySelector('main > section.api-error')).toBeNull();
  expect(root.textContent?.split(message).length - 1).toBe(1);
}

function assignmentData() {
  return {
    id: 42,
    course_id: 7,
    title: 'Assignment',
    description: 'Write a short response.',
    due_at: null,
    max_score: 10,
  };
}

function apiEnvelope<T>(data: T, businessCode = 'DESIGN_RESOURCE_RETRIEVED') {
  return {
    success: true,
    businessCode,
    message: 'Assignment loaded.',
    data,
    meta: {},
    traceId: 'st18-test',
  };
}

function uploadData() {
  return {
    id: 77,
    name: 'submission.txt',
    url: 'https://files.example/submission.txt',
    content_type: 'text/plain',
    size_bytes: 10,
    status: 'UPLOADED',
  };
}
