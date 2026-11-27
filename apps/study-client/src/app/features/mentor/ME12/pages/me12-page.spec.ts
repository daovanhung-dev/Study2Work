import { HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of, throwError } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import type {
  MentorSupportRequest,
  MentorUploadAsset,
} from '../../shared/models/mentor-api.models';
import { ME12SupportThreadService } from '../data-access/me12-support-thread.service';
import { ME12Page } from './me12-page';

@Component({ standalone: true, template: '<p>Mentor inbox reached</p>' })
class MentorInboxRouteStub {}

describe('ME12Page', () => {
  let detail: ReturnType<typeof vi.fn>;
  let reply: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    detail = vi.fn(() => of(apiEnvelope(request())));
    reply = vi.fn(() => of(apiEnvelope(request(), 'DESIGN_RESOURCE_UPDATED')));

    await TestBed.configureTestingModule({
      imports: [ME12Page, MentorInboxRouteStub],
      providers: [
        provideRouter([
          { path: 'mentor/support/:requestId', component: ME12Page },
          { path: 'mentor/support', component: MentorInboxRouteStub },
        ]),
        { provide: ME12SupportThreadService, useValue: { detail, reply } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('loads #59 thread data and keeps attachment URLs and #61 resolve gated', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/mentor/support/41', ME12Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(detail).toHaveBeenCalledExactlyOnceWith('41');
    expect(root.textContent).toContain('Learner One');
    expect(root.textContent).toContain('Need help with lesson access.');
    expect(root.textContent).toContain('screenshot.png');
    expect(root.textContent).not.toContain('files.example.test');
    expect(root.querySelector('.me12-attachments a')).toBeNull();
    expect(root.querySelector<HTMLButtonElement>('.me12-resolve-gate button')?.disabled).toBe(true);
    expect(root.querySelector<HTMLTextAreaElement>('#me12-message')?.disabled).toBe(false);
  });

  it('rejects an empty reply without calling API #60', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/mentor/support/41', ME12Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    submitReply(root, harness, '   ');
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(reply).not.toHaveBeenCalled();
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Câu trả lời không được để trống.',
    );
  });

  it('sends one #60 reply, confirms the returned message, then refreshes with #59', async () => {
    const before = request('OPEN', [message(301, 'Learner One', 'Need help with lesson access.')]);
    const updated = request('OPEN', [
      ...before.messages,
      message(302, 'Mentor One', 'Please try the course link again.'),
    ]);
    detail
      .mockReturnValueOnce(of(apiEnvelope(before)))
      .mockReturnValueOnce(of(apiEnvelope(updated)));
    reply.mockReturnValueOnce(of(apiEnvelope(updated, 'DESIGN_RESOURCE_UPDATED')));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/mentor/support/41', ME12Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    submitReply(root, harness, 'Please try the course link again.');
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(reply).toHaveBeenCalledExactlyOnceWith('41', 'Please try the course link again.');
    expect(detail).toHaveBeenCalledTimes(2);
    expect(detail).toHaveBeenNthCalledWith(1, '41');
    expect(detail).toHaveBeenNthCalledWith(2, '41');
    expect(root.textContent).toContain('Please try the course link again.');
    expect(root.querySelector('[role="status"]')?.textContent).toContain(
      'Câu trả lời đã được Study Server ghi nhận.',
    );
    expect(root.querySelector<HTMLButtonElement>('.me12-resolve-gate button')?.disabled).toBe(true);
  });

  it('requires a #59 reload before allowing another submit after an ambiguous #60 result', async () => {
    detail
      .mockReturnValueOnce(of(apiEnvelope(request())))
      .mockReturnValueOnce(of(apiEnvelope(request())));
    reply.mockReturnValueOnce(
      throwError(() => new HttpErrorResponse({ status: 0, statusText: 'Unknown Error' })),
    );

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/mentor/support/41', ME12Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    submitReply(root, harness, 'I will review the course access.');
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(reply).toHaveBeenCalledExactlyOnceWith('41', 'I will review the course access.');
    expect(root.querySelector<HTMLTextAreaElement>('#me12-message')?.disabled).toBe(true);
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Không gửi lặp lại khi chưa tải lại thread.',
    );
    root.querySelector<HTMLButtonElement>('.me12-reply button[type="button"]')?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(detail).toHaveBeenCalledTimes(2);
    expect(reply).toHaveBeenCalledTimes(1);
    expect(root.querySelector('[role="alert"]')?.textContent).toContain(
      'Thread đã được tải lại nhưng chưa xác nhận được câu trả lời trước đó.',
    );
    expect(root.querySelector<HTMLTextAreaElement>('#me12-message')?.disabled).toBe(false);
  });

  it('keeps reply unavailable for a resolved request', async () => {
    detail.mockReturnValueOnce(of(apiEnvelope(request('RESOLVED'))));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/mentor/support/41', ME12Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('form.me12-reply')).toBeNull();
    expect(root.textContent).toContain('Trả lời đang tạm khóa');
    expect(reply).not.toHaveBeenCalled();
  });

  it('does not call #59 for an invalid route ID', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/mentor/support/not-an-id', ME12Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(detail).not.toHaveBeenCalled();
    expect(harness.routeNativeElement?.textContent).toContain('Request ID không hợp lệ');
  });
});

function submitReply(root: HTMLElement, harness: RouterTestingHarness, text: string): void {
  const textarea = root.querySelector<HTMLTextAreaElement>('#me12-message');
  if (!textarea) throw new Error('ME-12 reply field is missing.');
  textarea.value = text;
  textarea.dispatchEvent(new Event('input', { bubbles: true }));
  harness.fixture.detectChanges();
  const button = root.querySelector<HTMLButtonElement>('button[type="submit"]');
  if (!button) throw new Error('ME-12 reply button is missing.');
  button.click();
}

function request(
  status = 'OPEN',
  messages: MentorSupportRequest['messages'] = [
    message(301, 'Learner One', 'Need help with lesson access.', [attachment()]),
  ],
): MentorSupportRequest {
  return {
    id: 41,
    course_id: 9,
    student: { id: 101, full_name: 'Learner One' },
    status,
    messages,
    created_at: '2026-11-27T02:00:00Z',
    resolved_at: status === 'RESOLVED' ? '2026-11-27T02:30:00Z' : null,
  };
}

function message(
  id: number,
  authorName: string,
  content: string,
  attachments: MentorUploadAsset[] = [],
): MentorSupportRequest['messages'][number] {
  return {
    id,
    author: { id: id === 301 ? 101 : 7, full_name: authorName },
    content,
    attachments,
    created_at: '2026-11-27T02:10:00Z',
  };
}

function attachment(): MentorUploadAsset {
  return {
    id: 501,
    name: 'screenshot.png',
    url: 'https://files.example.test/screenshot.png',
    content_type: 'image/png',
    size_bytes: 2048,
    status: 'UPLOADED',
  };
}

function apiEnvelope<T>(data: T, businessCode = 'DESIGN_RESOURCE_RETRIEVED') {
  return {
    success: true,
    businessCode,
    message: 'Support thread updated.',
    data,
    meta: {},
    traceId: 'me12-test',
  };
}
