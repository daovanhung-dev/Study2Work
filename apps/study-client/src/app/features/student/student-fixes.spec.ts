import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, Router, convertToParamMap, provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { StudentSessionService } from '../../core/auth/student-session.service';
import { StudentLayout } from '../../layouts/student/student-layout';
import { StudentPublicFrame } from '../../shared/ui/student-public-frame';
import { GS03CourseDetailService } from '../guest/GS03/data-access/gs03-course-detail.service';
import { ST04EnrollmentService } from './ST04/data-access/st04-enrollment.service';
import { ST04Page } from './ST04/pages/st04-page';
import { ST05Page } from './ST05/pages/st05-page';
import { ST08CoursesService } from './ST08/data-access/st08-courses.service';
import { ST08Page } from './ST08/pages/st08-page';
import { ST11LessonService } from './ST11/data-access/st11-lesson.service';
import { ST11Page } from './ST11/pages/st11-page';
import { ST20ProgressService } from './ST20/data-access/st20-progress.service';
import { ST20Page } from './ST20/pages/st20-page';
import { studentRoutes } from './student.route';

function envelope<T>(data: T, businessCode = 'DESIGN_RESOURCE_RETRIEVED') {
  return {
    success: true,
    businessCode,
    message: 'OK',
    data,
    traceId: 'trace-fix-verify',
  };
}

describe('Student screen fixes regression suite', () => {
  it('uses portal shell for ST-21 and ST-23 so header and footer render', () => {
    const layoutRoute = studentRoutes.find((r) => r.component === StudentLayout);
    const st21 = layoutRoute?.children?.find((r) => r.path === 'progress/:courseId');
    const st23 = layoutRoute?.children?.find((r) => r.path === 'discussions');
    expect(st21?.data?.['shell']).toBe('portal');
    expect(st23?.data?.['shell']).toBe('portal');
  });

  it('renders SVG bell icon instead of club glyph in StudentLayout portal header', async () => {
    const sessionMock = {
      isAuthenticated: () => true,
      profile: () => ({ full_name: 'Hoang Xuan Long', email: 'student@study2work.edu.vn' }),
      endLocalSession: vi.fn(),
    };
    await TestBed.configureTestingModule({
      imports: [StudentLayout],
      providers: [
        provideRouter([]),
        { provide: StudentSessionService, useValue: sessionMock },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(StudentLayout);
    fixture.componentInstance.shellMode = 'portal';
    fixture.detectChanges();

    const notice = fixture.nativeElement.querySelector('.portal-notice') as HTMLElement;
    expect(notice).not.toBeNull();
    expect(notice.textContent).not.toContain('♧');
    expect(notice.querySelector('svg')).not.toBeNull();
  });

  it('hides login/register buttons in StudentPublicFrame when authenticated', async () => {
    const sessionMock = {
      isAuthenticated: () => true,
      profile: () => ({ full_name: 'Hoang Xuan Long', email: 'student@study2work.edu.vn' }),
      endLocalSession: vi.fn(),
    };
    await TestBed.configureTestingModule({
      imports: [StudentPublicFrame],
      providers: [
        provideRouter([]),
        { provide: StudentSessionService, useValue: sessionMock },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(StudentPublicFrame);
    fixture.detectChanges();
    const header = fixture.nativeElement.querySelector('header') as HTMLElement;
    expect(header.textContent).toContain('Hoang Xuan Long');
    expect(header.textContent).toContain('Đăng xuất');
    expect(header.textContent).not.toContain('Đăng nhập');
    expect(header.textContent).not.toContain('Đăng ký');
  });

  it('navigates from ST-04 paid course to ST-05 /student/checkout/8 when clicking Tiếp tục thanh toán', async () => {
    const courseDetailMock = {
      getCourse: vi.fn(() =>
        of(
          envelope({
            items: [
              {
                id: 8,
                title: 'Paid Course',
                price: '599000.00',
                status: 'PUBLISHED',
              },
            ],
          }),
        ),
      ),
    };
    const enrollmentMock = {
      enrollmentStatus: vi.fn(() => {
        throw { status: 404 };
      }),
    };

    await TestBed.configureTestingModule({
      imports: [ST04Page],
      providers: [
        provideRouter([{ path: 'student/checkout/:courseId', component: ST05Page }]),
        { provide: ActivatedRoute, useValue: { paramMap: of(convertToParamMap({ courseId: '8' })) } },
        { provide: GS03CourseDetailService, useValue: courseDetailMock },
        { provide: ST04EnrollmentService, useValue: enrollmentMock },
      ],
    }).compileComponents();

    const router = TestBed.inject(Router);
    const navSpy = vi.spyOn(router, 'navigate');
    const fixture = TestBed.createComponent(ST04Page);
    fixture.componentInstance.course.set({
      id: 8,
      title: 'Paid Course',
      price: '599000.00',
      status: 'PUBLISHED',
    } as never);
    fixture.componentInstance.state.set('paid');
    fixture.detectChanges();

    const btn = fixture.nativeElement.querySelector('a.enrollment-return-button') as HTMLAnchorElement;
    expect(btn.textContent).toContain('Tiếp tục thanh toán');
    btn.click();
    expect(navSpy).toHaveBeenCalledWith(['/student/checkout', '8']);
  });

  it('supports COMPLETED filter and renders Đã hoàn thành label in ST-08', async () => {
    const coursesApi = {
      courses: vi.fn((_page: number, status?: 'ACTIVE' | 'COMPLETED') =>
        of(
          envelope({
            items: [
              {
                course_id: 2,
                name: 'Vue 3',
                enrollment_status: status ?? 'COMPLETED',
                course_status: 'PUBLISHED',
                enrolled_at: '2026-10-10T05:00:00Z',
              },
            ],
            pagination: { page: 1, size: 20, total: 1, total_pages: 1 },
          }),
        ),
      ),
    };

    await TestBed.configureTestingModule({
      imports: [ST08Page],
      providers: [provideRouter([]), { provide: ST08CoursesService, useValue: coursesApi }],
    }).compileComponents();

    const fixture = TestBed.createComponent(ST08Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Đã hoàn thành');
    expect(root.textContent).not.toContain('Trạng thái đang được xác nhận');

    fixture.componentInstance.changeFilter('completed');
    fixture.detectChanges();
    expect(coursesApi.courses).toHaveBeenCalledWith(1, 'COMPLETED');
  });

  it('renders video player, marks completion (#25) and loads next lesson (#27) on ST-11', async () => {
    const lessonApi = {
      lesson: vi.fn(() =>
        of(
          envelope({
            id: 1,
            course_id: 1,
            title: 'Bài 1',
            content: 'Nội dung bài 1',
            video_url: 'https://video.example.com/lesson1.mp4',
            order: 1,
            status: 'PUBLISHED',
          }),
        ),
      ),
      updateProgress: vi.fn(() =>
        of(
          envelope(
            {
              id: 1,
              course_id: 1,
              title: 'Bài 1',
              order: 1,
              status: 'PUBLISHED',
            },
            'DESIGN_RESOURCE_UPDATED',
          ),
        ),
      ),
      nextLesson: vi.fn(() =>
        of(
          envelope({
            id: 2,
            course_id: 1,
            title: 'Bài 2',
            order: 2,
            status: 'PUBLISHED',
          }),
        ),
      ),
    };

    await TestBed.configureTestingModule({
      imports: [ST11Page],
      providers: [
        provideRouter([]),
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: { paramMap: convertToParamMap({ lessonId: '1' }) },
            paramMap: of(convertToParamMap({ lessonId: '1' })),
          },
        },
        { provide: ST11LessonService, useValue: lessonApi },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(ST11Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('video.lesson-video-player')).not.toBeNull();
    expect(root.textContent).toContain('Bài tiếp theo: Bài 2');

    fixture.componentInstance.markCompleted();
    fixture.detectChanges();
    expect(lessonApi.updateProgress).toHaveBeenCalledWith('1', { percent: 100, completed: true });
    expect(root.textContent).toContain('Đã hoàn thành bài học');
  });

  it('renders real aggregate progress from API #21 on ST-20', async () => {
    const progressApi = {
      overallProgress: vi.fn(() =>
        of(
          envelope({
            total_enrolled_courses: 4,
            active_courses: 3,
            completed_courses: 1,
            total_lessons: 5,
            completed_lessons: 2,
            overall_progress_percent: 40,
            courses: [
              {
                course_id: 1,
                course_name: 'FastAPI Backend',
                enrollment_status: 'ACTIVE',
                total_lessons: 2,
                completed_lessons: 1,
                progress_percent: 50,
              },
            ],
          }),
        ),
      ),
      achievements: vi.fn(() =>
        of(
          envelope({
            items: [],
            pagination: { page: 1, size: 20, total: 0, total_pages: 0 },
          }),
        ),
      ),
    };

    await TestBed.configureTestingModule({
      imports: [ST20Page],
      providers: [provideRouter([]), { provide: ST20ProgressService, useValue: progressApi }],
    }).compileComponents();

    const fixture = TestBed.createComponent(ST20Page);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('40%');
    expect(root.textContent).toContain('2 / 5');
    expect(root.textContent).toContain('FastAPI Backend');
  });
});
