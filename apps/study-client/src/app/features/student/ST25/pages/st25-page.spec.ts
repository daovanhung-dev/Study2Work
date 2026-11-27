import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of, throwError } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ST25ThreadService } from '../data-access/st25-thread.service';
import type {
  StudentDiscussion,
  StudentDiscussionComment,
  StudentPage,
} from '../../shared/models/student-api.models';
import { ST25Page } from './st25-page';

describe('ST25Page', () => {
  let thread: ReturnType<typeof vi.fn>;
  let reply: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    thread = vi.fn(() => of(apiEnvelope(threadPage(), 'DESIGN_RESOURCE_RETRIEVED')));
    reply = vi.fn((_discussionId: string, content: string) =>
      of(apiEnvelope(threadPage([replyComment(content)]), 'DESIGN_RESOURCE_CREATED')),
    );

    await TestBed.configureTestingModule({
      imports: [ST25Page],
      providers: [
        provideRouter([{ path: 'student/discussions/:discussionId', component: ST25Page }]),
        { provide: ST25ThreadService, useValue: { thread, reply } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('loads and renders the matching thread and its empty-reply state', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/discussions/91', ST25Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(thread).toHaveBeenCalledExactlyOnceWith('91');
    expect(root.querySelector('h1')?.textContent).toContain('Vue de cycle de travail');
    expect(root.textContent).toContain('Học viên An');
    expect(root.textContent).toContain('Chưa có phản hồi nào.');
    expect(root.querySelector('[role="status"]')).toBeNull();
  });

  it('trims a reply and shows it only after #41 success and #42 refresh', async () => {
    thread
      .mockReturnValueOnce(of(apiEnvelope(threadPage(), 'DESIGN_RESOURCE_RETRIEVED')))
      .mockReturnValueOnce(
        of(apiEnvelope(threadPage([replyComment('Ý kiến đã kiểm tra')]), 'DESIGN_RESOURCE_RETRIEVED')),
      );
    reply.mockReturnValueOnce(
      of(apiEnvelope(threadPage([replyComment('Ý kiến đã kiểm tra')]), 'DESIGN_RESOURCE_CREATED')),
    );

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/discussions/91', ST25Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    const input = root.querySelector<HTMLTextAreaElement>('textarea[name="replyContent"]');
    expect(input).not.toBeNull();
    if (input) {
      input.value = '  Ý kiến đã kiểm tra  ';
      input.dispatchEvent(new Event('input', { bubbles: true }));
    }
    harness.fixture.detectChanges();
    root.querySelector<HTMLButtonElement>('button[type="submit"]')?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(reply).toHaveBeenCalledExactlyOnceWith('91', 'Ý kiến đã kiểm tra');
    expect(thread).toHaveBeenNthCalledWith(1, '91');
    expect(thread).toHaveBeenNthCalledWith(2, '91');
    expect(root.textContent).toContain('Ý kiến đã kiểm tra');
    expect(root.querySelector('[role="status"]')?.textContent).toContain('Phản hồi đã được gửi.');
    expect(input?.value).toBe('');
  });

  it('offers a thread retry and recovers after the initial #42 request fails', async () => {
    thread
      .mockReturnValueOnce(throwError(() => new Error('temporary failure')))
      .mockReturnValueOnce(of(apiEnvelope(threadPage(), 'DESIGN_RESOURCE_RETRIEVED')));

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/student/discussions/91', ST25Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent?.trim()).toBeTruthy();
    root.querySelector<HTMLButtonElement>('.api-error button')?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(thread).toHaveBeenCalledTimes(2);
    expect(root.querySelector('h1')?.textContent).toContain('Vue de cycle de travail');
    expect(root.querySelector('[role="alert"]')).toBeNull();
  });

  it('locks resubmission after an ambiguous #41 failure and allows a read-only #42 check', async () => {
    reply.mockReturnValueOnce(
      throwError(() => new HttpErrorResponse({ status: 0, statusText: 'Network error' })),
    );

    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/student/discussions/91', ST25Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    page.replyContent = 'A reply';
    page.sendReply();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(reply).toHaveBeenCalledExactlyOnceWith('91', 'A reply');
    expect(root.querySelector('.st25-ambiguous-result')?.textContent).toContain(
      'nút gửi đang khóa để tránh tạo bản trùng',
    );
    expect(root.querySelector<HTMLTextAreaElement>('textarea[name="replyContent"]')?.disabled).toBe(true);
    expect(root.querySelector<HTMLButtonElement>('button[type="submit"]')?.disabled).toBe(true);

    root.querySelector<HTMLButtonElement>('.st25-ambiguous-result button')?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(thread).toHaveBeenCalledTimes(2);
    expect(reply).toHaveBeenCalledTimes(1);
    expect(root.querySelector<HTMLButtonElement>('button[type="submit"]')?.disabled).toBe(true);
  });
});

function threadPage(comments: StudentDiscussionComment[] = []): StudentPage<StudentDiscussion> {
  return {
    items: [
      {
        id: 91,
        course_id: 12,
        title: 'Vue de cycle de travail',
        content: 'Câu hỏi về nhịp độ học tập.',
        author: { id: 7, full_name: 'Học viên An', avatar_url: null },
        status: 'ACTIVE',
        comments,
      },
    ],
    pagination: { page: 1, size: 1, total: 1, total_pages: 1 },
  };
}

function replyComment(content: string): StudentDiscussionComment {
  return {
    id: 301,
    discussion_id: 91,
    content,
    author: { id: 8, full_name: 'Học viên Bình', avatar_url: null },
    created_at: '2026-11-26T09:30:00Z',
  };
}

function apiEnvelope<T>(data: T, businessCode: string) {
  return {
    success: true,
    businessCode,
    message: 'Discussion data loaded.',
    data,
    meta: {},
    traceId: 'st25-test',
  };
}
