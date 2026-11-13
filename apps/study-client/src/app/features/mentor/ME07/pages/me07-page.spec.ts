import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, Router, convertToParamMap } from '@angular/router';
import { of, throwError } from 'rxjs';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { Me07EditorService } from '../data-access/me07-editor.service';
import type { Me07ContentNodeDto } from '../models/me07-editor.models';
import { ME07Page } from './me07-page';

describe('ME07Page', () => {
  const existingNode: Me07ContentNodeDto = {
    id: 25,
    course_id: 101,
    content_type: 'LESSON',
    title: 'Bài 2: Tối ưu truy vấn SQL',
    payload: { summary: 'Tóm tắt SQL', body: 'Nội dung chi tiết SQL' },
    status: 'PENDING_REVIEW',
    parent_id: null,
    order: 1,
  };

  const getCourseContentsMock = vi.fn();
  const createContentMock = vi.fn();
  const updateContentMock = vi.fn();
  const navigateMock = vi.fn().mockResolvedValue(true);

  function configureRoute(params: Record<string, string>) {
    TestBed.configureTestingModule({
      imports: [ME07Page],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: convertToParamMap(params),
            },
          },
        },
        {
          provide: Router,
          useValue: { navigate: navigateMock },
        },
        {
          provide: Me07EditorService,
          useValue: {
            getCourseContents: getCourseContentsMock,
            createContent: createContentMock,
            updateContent: updateContentMock,
          },
        },
      ],
    });
  }

  beforeEach(() => {
    getCourseContentsMock.mockReset();
    createContentMock.mockReset();
    updateContentMock.mockReset();
    navigateMock.mockClear();
  });

  it('starts in create mode when contentId is absent and submits POST #50', async () => {
    createContentMock.mockReturnValue(
      of({
        success: true,
        businessCode: 'DESIGN_RESOURCE_CREATED',
        message: 'Content created.',
        data: { ...existingNode, id: 30, title: 'Chương mới' },
        meta: {},
        traceId: 'trace-create-50',
      }),
    );

    configureRoute({ courseId: '101' });
    await TestBed.compileComponents();

    const fixture = TestBed.createComponent(ME07Page);
    fixture.detectChanges();

    expect(fixture.componentInstance.mode()).toBe('create');
    expect(getCourseContentsMock).not.toHaveBeenCalled();

    fixture.componentInstance.currentDraft.set({
      title: 'Chương mới',
      contentType: 'SECTION',
      summaryText: 'Mô tả chương',
      bodyText: 'Nội dung chương',
    });

    fixture.componentInstance.submitForm();

    expect(createContentMock).toHaveBeenCalledWith({
      course_id: 101,
      content_type: 'SECTION',
      title: 'Chương mới',
      payload: {
        summary: 'Mô tả chương',
        body: 'Nội dung chương',
      },
    });
  });

  it('hydrates existing node via GET #49 in edit mode and submits PUT #51', async () => {
    getCourseContentsMock.mockReturnValue(
      of({
        success: true,
        businessCode: 'DESIGN_RESOURCE_RETRIEVED',
        message: 'OK',
        data: [existingNode],
        meta: {},
        traceId: 'trace-49',
      }),
    );
    updateContentMock.mockReturnValue(
      of({
        success: true,
        businessCode: 'DESIGN_RESOURCE_UPDATED',
        message: 'Content updated.',
        data: { ...existingNode, title: 'Bài 2 (Đã cập nhật)' },
        meta: {},
        traceId: 'trace-51',
      }),
    );

    configureRoute({ courseId: '101', contentId: '25' });
    await TestBed.compileComponents();

    const fixture = TestBed.createComponent(ME07Page);
    fixture.detectChanges();

    expect(fixture.componentInstance.mode()).toBe('edit');
    expect(getCourseContentsMock).toHaveBeenCalledWith(101);
    expect(fixture.componentInstance.currentDraft().title).toBe('Bài 2: Tối ưu truy vấn SQL');

    fixture.componentInstance.currentDraft.update((prev) => ({
      ...prev,
      title: 'Bài 2 (Đã cập nhật)',
    }));
    expect(fixture.componentInstance.isDirty()).toBe(true);

    fixture.componentInstance.submitForm();

    expect(updateContentMock).toHaveBeenCalledWith(25, {
      content_type: 'LESSON',
      title: 'Bài 2 (Đã cập nhật)',
      payload: {
        summary: 'Tóm tắt SQL',
        body: 'Nội dung chi tiết SQL',
      },
    });
  });

  it('preserves user draft when PUT #51 fails with 422 validation error and prompts before discarding dirty changes', async () => {
    getCourseContentsMock.mockReturnValue(
      of({
        success: true,
        businessCode: 'DESIGN_RESOURCE_RETRIEVED',
        message: 'OK',
        data: [existingNode],
        meta: {},
        traceId: 'trace-49',
      }),
    );
    updateContentMock.mockReturnValue(
      throwError(
        () =>
          new HttpErrorResponse({
            status: 422,
            error: { message: 'Dữ liệu đầu vào không hợp lệ.' },
          }),
      ),
    );

    configureRoute({ courseId: '101', contentId: '25' });
    await TestBed.compileComponents();

    const fixture = TestBed.createComponent(ME07Page);
    fixture.detectChanges();

    fixture.componentInstance.currentDraft.update((prev) => ({
      ...prev,
      title: 'Tiêu đề đang sửa dở',
    }));

    fixture.componentInstance.submitForm();
    expect(fixture.componentInstance.currentDraft().title).toBe('Tiêu đề đang sửa dở');
    expect(fixture.componentInstance.validationError()).toContain('Dữ liệu đầu vào không hợp lệ');

    fixture.componentInstance.requestCancelOrBack();
    expect(fixture.componentInstance.showCancelConfirm()).toBe(true);
    expect(navigateMock).not.toHaveBeenCalled();
  });
});
