import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ME07ContentEditorService } from '../data-access/me07-content-editor.service';
import type { MentorContent } from '../../shared/models/mentor-api.models';
import { ME07Page } from './me07-page';

describe('ME07Page', () => {
  let editor: {
    list: ReturnType<typeof vi.fn>;
    create: ReturnType<typeof vi.fn>;
    update: ReturnType<typeof vi.fn>;
  };

  beforeEach(async () => {
    editor = { list: vi.fn(), create: vi.fn(), update: vi.fn() };
    editor.list.mockReturnValue(of(apiEnvelope([content()])));

    await TestBed.configureTestingModule({
      imports: [ME07Page],
      providers: [
        provideRouter([
          { path: 'mentor/courses/:courseId/content/new', component: ME07Page },
          { path: 'mentor/courses/:courseId/content/:contentId', component: ME07Page },
        ]),
        { provide: ME07ContentEditorService, useValue: editor },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('keeps create disabled and never sends #50 with an unapproved payload', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/mentor/courses/8/content/new', ME07Page);

    const root = harness.routeNativeElement as HTMLElement;
    const saveButton = findSaveButton(root);
    expect(editor.list).toHaveBeenCalledWith('8');
    expect(saveButton.disabled).toBe(true);
    expect(root.textContent?.toLowerCase()).toContain('schema payload chưa được duyệt');

    const submit = new Event('submit', { bubbles: true, cancelable: true });
    root.querySelector('form')?.dispatchEvent(submit);
    harness.fixture.detectChanges();

    expect(submit.defaultPrevented).toBe(true);
    expect(editor.create).not.toHaveBeenCalled();
    expect(editor.update).not.toHaveBeenCalled();
  });

  it('keeps edit disabled and never sends #51 with a free-form replacement', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/mentor/courses/8/content/17', ME07Page);

    const root = harness.routeNativeElement as HTMLElement;
    expect((root.querySelector('#me07-title') as HTMLInputElement).value).toBe('Lesson content');
    expect(findSaveButton(root).disabled).toBe(true);
    expect(root.querySelector('textarea')).toBeNull();

    const submit = new Event('submit', { bubbles: true, cancelable: true });
    root.querySelector('form')?.dispatchEvent(submit);
    harness.fixture.detectChanges();

    expect(submit.defaultPrevented).toBe(true);
    expect(editor.update).not.toHaveBeenCalled();
    expect(editor.create).not.toHaveBeenCalled();
  });
});

function findSaveButton(root: HTMLElement): HTMLButtonElement {
  const button = Array.from(root.querySelectorAll('button')).find((candidate) =>
    candidate.textContent?.includes('Lưu bản nháp'),
  );
  if (!(button instanceof HTMLButtonElement)) throw new Error('ME-07 save button is missing.');
  return button;
}

function content(): MentorContent {
  return {
    id: '17',
    course_id: '8',
    content_type: 'lesson',
    title: 'Lesson content',
    payload: { text: 'not rendered by the gated editor' },
    status: 'PENDING_REVIEW',
    parent_id: null,
    order: 1,
  };
}

function apiEnvelope<T>(data: T) {
  return { success: true, businessCode: 'DESIGN_RESOURCE_RETRIEVED', message: '', data, meta: {}, traceId: 'me07-test' };
}
