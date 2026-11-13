import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, Router, convertToParamMap } from '@angular/router';
import { of, throwError } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { Me06ContentService } from '../data-access/me06-content.service';
import type { ContentNodeDto } from '../models/me06-content.models';
import { ME06Page } from './me06-page';

describe('ME06Page', () => {
  const sampleNodes: ContentNodeDto[] = [
    {
      id: 10,
      course_id: 101,
      content_type: 'SECTION',
      title: 'Chương 1: Kiến trúc hệ thống',
      payload: {},
      status: 'PUBLISHED',
      parent_id: null,
      order: 0,
    },
    {
      id: 11,
      course_id: 101,
      content_type: 'LESSON',
      title: 'Bài 1.1: Thiết kế cơ sở dữ liệu',
      payload: { body: 'Nội dung bài học' },
      status: 'PENDING_REVIEW',
      parent_id: 10,
      order: 0,
    },
  ];

  const getCourseContentsMock = vi.fn();
  const navigateMock = vi.fn().mockResolvedValue(true);

  function setupRoute(courseIdParam: string) {
    TestBed.configureTestingModule({
      imports: [ME06Page],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: convertToParamMap({ courseId: courseIdParam }),
            },
          },
        },
        {
          provide: Router,
          useValue: { navigate: navigateMock },
        },
        {
          provide: Me06ContentService,
          useValue: { getCourseContents: getCourseContentsMock },
        },
      ],
    });
  }

  beforeEach(() => {
    getCourseContentsMock.mockReset();
    navigateMock.mockClear();
  });

  it('calls API #49 and renders hierarchical content tree with truthful PUBLISHED vs PENDING_REVIEW badges', async () => {
    getCourseContentsMock.mockReturnValue(
      of({
        success: true,
        businessCode: 'DESIGN_RESOURCE_RETRIEVED',
        message: 'Course content retrieved.',
        data: sampleNodes,
        meta: {},
        traceId: 'trace-me06-1',
      }),
    );

    setupRoute('101');
    await TestBed.compileComponents();

    const fixture = TestBed.createComponent(ME06Page);
    fixture.detectChanges();

    expect(getCourseContentsMock).toHaveBeenCalledWith(101);
    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Chương 1: Kiến trúc hệ thống');
    expect(root.textContent).toContain('Bài 1.1: Thiết kế cơ sở dữ liệu');
    expect(root.textContent).toContain('Đã xuất bản');
    expect(root.textContent).toContain('Chờ duyệt (Bản nháp)');
  });

  it('rejects non-int64 courseId without calling API #49', async () => {
    setupRoute('invalid-slug');
    await TestBed.compileComponents();

    const fixture = TestBed.createComponent(ME06Page);
    fixture.detectChanges();

    expect(getCourseContentsMock).not.toHaveBeenCalled();
    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Tham số khóa học không hợp lệ');
  });

  it('navigates to ME-07 edit and ME-08 publish/delete actions with courseId context', async () => {
    getCourseContentsMock.mockReturnValue(
      of({
        success: true,
        businessCode: 'DESIGN_RESOURCE_RETRIEVED',
        message: 'OK',
        data: sampleNodes,
        meta: {},
        traceId: 'trace-me06-2',
      }),
    );

    setupRoute('101');
    await TestBed.compileComponents();

    const fixture = TestBed.createComponent(ME06Page);
    fixture.detectChanges();

    fixture.componentInstance.onNodeAction({ node: sampleNodes[1], action: 'edit' });
    expect(navigateMock).toHaveBeenCalledWith(['/mentor/courses', 101, 'content', 11]);

    fixture.componentInstance.onNodeAction({ node: sampleNodes[1], action: 'publish' });
    expect(navigateMock).toHaveBeenCalledWith(['/mentor/content', 11, 'actions'], {
      queryParams: { courseId: 101, action: 'publish' },
    });
  });

  it('maps 403 error from API #49 to forbidden state', async () => {
    getCourseContentsMock.mockReturnValue(
      throwError(
        () =>
          new HttpErrorResponse({
            status: 403,
            error: { message: 'Access denied.', traceId: 'trace-403' },
          }),
      ),
    );

    setupRoute('101');
    await TestBed.compileComponents();

    const fixture = TestBed.createComponent(ME06Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Truy cập bị từ chối (403)');
  });
});
