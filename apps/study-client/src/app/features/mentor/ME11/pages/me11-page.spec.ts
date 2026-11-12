import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, Router, convertToParamMap, provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { Me11SupportService } from '../data-access/me11-support.service';
import { ME11Page } from './me11-page';

describe('ME11Page', () => {
  const sampleCoursesEnvelope = {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'OK',
    data: {
      items: [{ id: 101, title: 'Thiết kế Hệ thống', status: 'PUBLISHED' }],
      pagination: { page: 1, size: 50, total: 1, total_pages: 1 },
    },
    meta: {},
    traceId: 'trace-me11-courses',
  };

  const sampleRequestsEnvelope = {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'OK',
    data: [
      {
        id: 701,
        course_id: 101,
        student: { id: 3001, full_name: 'Nguyễn Văn A', avatar_url: null },
        status: 'OPEN',
        messages: [
          {
            id: 1,
            author: { id: 3001, full_name: 'Nguyễn Văn A' },
            content: 'Em cần hỗ trợ về bài tập tuần 2 ạ.',
            attachments: [],
            created_at: '2026-11-12T09:00:00Z',
          },
        ],
        created_at: '2026-11-12T09:00:00Z',
        resolved_at: null,
      },
    ],
    meta: {},
    traceId: 'trace-me11-requests',
  };

  function setupTest() {
    const serviceStub = {
      getMentorCourses: vi.fn().mockReturnValue(of(sampleCoursesEnvelope)),
      getSupportRequests: vi.fn().mockReturnValue(of(sampleRequestsEnvelope)),
    };

    TestBed.configureTestingModule({
      imports: [ME11Page],
      providers: [
        provideRouter([]),
        { provide: Me11SupportService, useValue: serviceStub },
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: convertToParamMap({}),
              queryParamMap: convertToParamMap({ courseId: '101', status: 'OPEN' }),
            },
          },
        },
      ],
    });

    return { serviceStub, router: TestBed.inject(Router) };
  }

  it('loads mentor courses (#46) and support requests (#58) and renders request cards', () => {
    const { serviceStub } = setupTest();
    const fixture = TestBed.createComponent(ME11Page);
    fixture.detectChanges();

    expect(serviceStub.getMentorCourses).toHaveBeenCalledTimes(1);
    expect(serviceStub.getSupportRequests).toHaveBeenCalledWith({
      course_id: 101,
      status: 'OPEN',
    });
    expect(fixture.componentInstance.screenState()).toBe('ready');

    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Yêu cầu #701');
    expect(text).toContain('Nguyễn Văn A');
    expect(text).toContain('Em cần hỗ trợ về bài tập tuần 2 ạ.');
  });

  it('reloads API #58 when changing status tab', () => {
    const { serviceStub } = setupTest();
    const fixture = TestBed.createComponent(ME11Page);
    fixture.detectChanges();

    fixture.componentInstance.onStatusChange('RESOLVED');
    expect(serviceStub.getSupportRequests).toHaveBeenLastCalledWith({
      course_id: 101,
      status: 'RESOLVED',
    });
  });

  it('navigates to ME-12 (/mentor/support/:requestId) when clicking a support request', () => {
    const { router } = setupTest();
    const navSpy = vi.spyOn(router, 'navigate').mockResolvedValue(true);

    const fixture = TestBed.createComponent(ME11Page);
    fixture.detectChanges();

    fixture.componentInstance.openSupportThread(701);
    expect(navSpy).toHaveBeenCalledWith(['/mentor/support', 701]);
  });
});
