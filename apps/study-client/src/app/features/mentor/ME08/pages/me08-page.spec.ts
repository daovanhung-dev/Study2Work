import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, Router, convertToParamMap } from '@angular/router';
import { of, throwError } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { Me08ActionsService } from '../data-access/me08-actions.service';
import type { Me08ContentNodeDto } from '../models/me08-actions.models';
import { ME08Page } from './me08-page';

describe('ME08Page', () => {
  const approvedNode: Me08ContentNodeDto = {
    id: 40,
    course_id: 101,
    content_type: 'LESSON',
    title: 'Bài 4: Kiến trúc Microservices',
    payload: {},
    status: 'APPROVED',
    parent_id: null,
    order: 2,
  };

  const getCourseContentsMock = vi.fn();
  const setPublishStateMock = vi.fn();
  const deleteContentMock = vi.fn();
  const navigateMock = vi.fn().mockResolvedValue(true);

  function configureRoute(params: Record<string, string>, queryParams: Record<string, string>) {
    TestBed.configureTestingModule({
      imports: [ME08Page],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: convertToParamMap(params),
              queryParamMap: convertToParamMap(queryParams),
            },
          },
        },
        {
          provide: Router,
          useValue: { navigate: navigateMock },
        },
        {
          provide: Me08ActionsService,
          useValue: {
            getCourseContents: getCourseContentsMock,
            setPublishState: setPublishStateMock,
            deleteContent: deleteContentMock,
          },
        },
      ],
    });
  }

  beforeEach(() => {
    getCourseContentsMock.mockReset();
    setPublishStateMock.mockReset();
    deleteContentMock.mockReset();
    navigateMock.mockClear();
  });

  it('hydrates target node from GET #49 and supports dialog mode when dialog=1', async () => {
    getCourseContentsMock.mockReturnValue(
      of({
        success: true,
        businessCode: 'DESIGN_RESOURCE_RETRIEVED',
        message: 'OK',
        data: [approvedNode],
        meta: {},
        traceId: 'trace-49',
      }),
    );

    configureRoute({ contentId: '40' }, { courseId: '101', action: 'publish', dialog: '1' });
    await TestBed.compileComponents();

    const fixture = TestBed.createComponent(ME08Page);
    fixture.detectChanges();

    expect(fixture.componentInstance.isDialogMode()).toBe(true);
    expect(fixture.componentInstance.inspection()?.canPublish).toBe(true);
    expect(fixture.componentInstance.inspection()?.canDelete).toBe(true);
  });

  it('calls PATCH #52 { published: true } and refreshes GET #49 afterwards', async () => {
    getCourseContentsMock.mockReturnValue(
      of({
        success: true,
        businessCode: 'DESIGN_RESOURCE_RETRIEVED',
        message: 'OK',
        data: [approvedNode],
        meta: {},
        traceId: 'trace-49',
      }),
    );
    setPublishStateMock.mockReturnValue(
      of({
        success: true,
        businessCode: 'DESIGN_RESOURCE_UPDATED',
        message: 'Updated',
        data: { ...approvedNode, status: 'PUBLISHED' },
        meta: {},
        traceId: 'trace-52',
      }),
    );

    configureRoute({ contentId: '40' }, { courseId: '101', action: 'publish' });
    await TestBed.compileComponents();

    const fixture = TestBed.createComponent(ME08Page);
    fixture.detectChanges();

    fixture.componentInstance.executePublishState(true);

    expect(setPublishStateMock).toHaveBeenCalledWith(40, { published: true });
    expect(getCourseContentsMock).toHaveBeenCalledTimes(2);
    expect(fixture.componentInstance.screenState()).toBe('mutation-success');
  });

  it('separates mutation success from GET #49 refresh failure after DELETE #53', async () => {
    getCourseContentsMock
      .mockReturnValueOnce(
        of({
          success: true,
          businessCode: 'DESIGN_RESOURCE_RETRIEVED',
          message: 'OK',
          data: [approvedNode],
          meta: {},
          traceId: 'trace-49-init',
        }),
      )
      .mockReturnValueOnce(
        throwError(() => new HttpErrorResponse({ status: 500, error: { message: 'DB error' } })),
      );

    deleteContentMock.mockReturnValue(
      of({
        success: true,
        businessCode: 'DESIGN_RESOURCE_DELETED',
        message: 'Deleted',
        data: { id: 40, status: 'deleted', deleted_at: '2026-11-12T10:00:00Z' },
        meta: {},
        traceId: 'trace-53',
      }),
    );

    configureRoute({ contentId: '40' }, { courseId: '101', action: 'delete' });
    await TestBed.compileComponents();

    const fixture = TestBed.createComponent(ME08Page);
    fixture.detectChanges();

    fixture.componentInstance.executeDelete();

    expect(deleteContentMock).toHaveBeenCalledWith(40);
    expect(fixture.componentInstance.screenState()).toBe('refresh-error');
    expect(fixture.componentInstance.outcomeMessage()).toContain('Đã xóa mềm nội dung #40');
    expect(fixture.componentInstance.errorMessage()).toContain('tải lại cây nội dung (#49) bị lỗi');
  });
});
