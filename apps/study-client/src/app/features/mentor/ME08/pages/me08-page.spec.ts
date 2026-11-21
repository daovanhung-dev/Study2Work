import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ME08ContentActionsService } from '../data-access/me08-content-actions.service';
import type { MentorContent } from '../../shared/models/mentor-api.models';
import { ME08Page } from './me08-page';

describe('ME08Page', () => {
  let actions: {
    content: ReturnType<typeof vi.fn>;
    publish: ReturnType<typeof vi.fn>;
    delete: ReturnType<typeof vi.fn>;
  };
  let originalHistoryState: unknown;

  beforeEach(async () => {
    originalHistoryState = history.state;
    history.replaceState({ courseId: '8' }, '', '/');
    actions = { content: vi.fn(), publish: vi.fn(), delete: vi.fn() };
    actions.content.mockReturnValue(of(apiEnvelope([content('APPROVED')])));

    await TestBed.configureTestingModule({
      imports: [ME08Page],
      providers: [
        provideRouter([]),
        {
          provide: ActivatedRoute,
          useValue: { paramMap: of({ get: (name: string) => name === 'contentId' ? '17' : null }) },
        },
        { provide: ME08ContentActionsService, useValue: actions },
      ],
    }).compileComponents();
  });

  afterEach(() => {
    TestBed.resetTestingModule();
    history.replaceState(originalHistoryState, '', '/');
  });

  it('keeps publish and delete disabled for APPROVED content', () => {
    const fixture = TestBed.createComponent(ME08Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(actions.content).toHaveBeenCalledWith('8');
    expect(findButton(root, 'Xuất bản').disabled).toBe(true);
    expect(findButton(root, 'Gỡ nội dung').disabled).toBe(true);
    expect(root.textContent).toContain('lifecycle, xác nhận và chính sách phụ thuộc chưa được duyệt');

    findButton(root, 'Xuất bản').click();
    findButton(root, 'Gỡ nội dung').click();

    expect(actions.publish).not.toHaveBeenCalled();
    expect(actions.delete).not.toHaveBeenCalled();
  });

  it('keeps unpublish and delete disabled for PUBLISHED content', () => {
    actions.content.mockReturnValue(of(apiEnvelope([content('PUBLISHED')])));
    const fixture = TestBed.createComponent(ME08Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(findButton(root, 'Đưa về APPROVED').disabled).toBe(true);
    expect(findButton(root, 'Gỡ nội dung').disabled).toBe(true);
    expect(actions.publish).not.toHaveBeenCalled();
    expect(actions.delete).not.toHaveBeenCalled();
  });
});

function findButton(root: HTMLElement, text: string): HTMLButtonElement {
  const button = Array.from(root.querySelectorAll('button')).find((candidate) =>
    candidate.textContent?.includes(text),
  );
  if (!(button instanceof HTMLButtonElement)) throw new Error('ME-08 action button is missing.');
  return button;
}

function content(status: string): MentorContent {
  return {
    id: '17',
    course_id: '8',
    content_type: 'lesson',
    title: 'Lesson content',
    payload: {},
    status,
    parent_id: null,
    order: 1,
  };
}

function apiEnvelope<T>(data: T) {
  return { success: true, businessCode: 'DESIGN_RESOURCE_RETRIEVED', message: '', data, meta: {}, traceId: 'me08-test' };
}
