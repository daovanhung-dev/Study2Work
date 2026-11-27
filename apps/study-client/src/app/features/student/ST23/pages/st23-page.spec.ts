import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ST23DiscussionsService } from '../data-access/st23-discussions.service';
import type { StudentDiscussion, StudentPage } from '../../shared/models/student-api.models';
import { ST23Page } from './st23-page';

describe('ST23Page', () => {
  let discussions: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    discussions = vi.fn().mockReturnValue(of(apiEnvelope(discussionPage())));

    await TestBed.configureTestingModule({
      imports: [ST23Page],
      providers: [
        provideRouter([{ path: 'student/discussions', component: ST23Page }]),
        { provide: ST23DiscussionsService, useValue: { discussions } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('keeps returned rows and offers a retry when COUNT and LIST disagree', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/student/discussions', ST23Page);
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(discussions).toHaveBeenCalledExactlyOnceWith(null, 1);
    expect(page.snapshotMismatch()).toBe(true);
    expect(page.discussions()).toHaveLength(1);
    expect(root.querySelector('.discussion-list h2')?.textContent).toContain('Current topic');
    expect(root.querySelector('[role="status"]')?.textContent).toContain(
      'Tổng số và danh sách thảo luận trên trang chưa đồng nhất.',
    );
    expect(root.querySelector('nav[aria-label="Phân trang"]')).toBeNull();

    const retry = Array.from(root.querySelectorAll('button')).find((button) =>
      button.textContent?.includes('Tải lại danh sách'),
    );
    expect(retry).toBeDefined();
    retry?.click();
    await harness.fixture.whenStable();
    harness.fixture.detectChanges();

    expect(discussions).toHaveBeenCalledTimes(2);
    expect(page.discussions()).toHaveLength(1);
  });
});

function discussionPage(): StudentPage<StudentDiscussion> {
  return {
    items: [
      {
        id: 31,
        course_id: 42,
        title: 'Current topic',
        content: 'A live discussion',
        author: { id: 7, full_name: 'Learner', avatar_url: null },
        status: 'ACTIVE',
        comments: [],
      },
    ],
    pagination: { page: 1, size: 20, total: 2, total_pages: 1 },
  };
}

function apiEnvelope<T>(data: T) {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'Discussion list loaded.',
    data,
    meta: {},
    traceId: 'st23-test',
  };
}
