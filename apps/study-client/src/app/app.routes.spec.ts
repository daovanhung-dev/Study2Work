import { provideHttpClient } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { beforeEach, describe, expect, it } from 'vitest';

import { App } from './app';
import { routes } from './app.routes';
import { AdminLayout } from './layouts/admin/admin-layout';
import { MentorLayout } from './layouts/mentor/mentor-layout';
import { SystemLayout } from './layouts/system/system-layout';

describe('Study app routes', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideHttpClient(), provideRouter(routes)],
    }).compileComponents();
  });

  it('renders the readiness scaffold at the root route', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/', SystemLayout);

    expect(harness.routeNativeElement?.textContent).toContain('Khung ứng dụng đã sẵn sàng');
  });

  it('renders AD-01 at /admin without the root scaffold', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/admin', AdminLayout);

    const routedText = harness.routeNativeElement?.textContent ?? '';
    expect(routedText).toContain('Bảng điều khiển quản trị hệ thống');
    expect(routedText).not.toContain('Khung ứng dụng đã sẵn sàng');
  });

  it('routes Mentor Phase 1 screens (ME-06, ME-07, ME-08) under /mentor', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/mentor/courses/101/content/new', MentorLayout);

    const routedText = harness.routeNativeElement?.textContent ?? '';
    expect(routedText).toContain('Tạo nội dung khóa học mới');
  });

  it('routes Mentor Phase 2 screens (ME-09, ME-10) under /mentor/submissions', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/mentor/submissions', MentorLayout);
    expect(harness.routeNativeElement?.textContent).toContain('Danh sách bài nộp cần chấm điểm');

    await harness.navigateByUrl('/mentor/submissions/9001', MentorLayout);
    expect(harness.routeNativeElement?.textContent).toContain(
      'Đánh giá bài tập và phản hồi học viên',
    );
  });

  it('routes Mentor Phase 3 screens (ME-11, ME-12) under /mentor/support', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/mentor/support', MentorLayout);
    expect(harness.routeNativeElement?.textContent).toContain(
      'Hộp thư hỗ trợ và giải đáp thắc mắc học viên',
    );

    await harness.navigateByUrl('/mentor/support/701', MentorLayout);
    expect(harness.routeNativeElement?.textContent).toContain(
      'Trao đổi và đóng yêu cầu hỗ trợ học viên',
    );
  });

  it('routes Mentor Phase 4 screens (ME-16, ME-17, ME-18) under /mentor/courses/:courseId', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/mentor/courses/101/progress', MentorLayout);
    expect(harness.routeNativeElement?.textContent).toContain('Tiến độ toàn khóa học');

    await harness.navigateByUrl('/mentor/courses/101/students/501/progress', MentorLayout);
    expect(harness.routeNativeElement?.textContent).toContain('Tiến độ từng học viên');

    await harness.navigateByUrl('/mentor/courses/101/analytics', MentorLayout);
    expect(harness.routeNativeElement?.textContent).toContain('Analytics hoạt động khóa học');
  });

  it('routes Mentor Phase 5 screens (ME-13, ME-14, ME-15) under /mentor/notifications', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/mentor/notifications/recipients', MentorLayout);
    expect(harness.routeNativeElement?.textContent).toContain('Chọn người nhận thông báo');

    await harness.navigateByUrl('/mentor/notifications/create?recipients=501', MentorLayout);
    expect(harness.routeNativeElement?.textContent).toContain('Tạo và phát hành thông báo');

    await harness.navigateByUrl('/mentor/notifications/status', MentorLayout);
    expect(harness.routeNativeElement?.textContent).toContain('Trạng thái gửi thông báo');
  });

  it('keeps the root component as a router outlet only', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('router-outlet')).not.toBeNull();
    expect(root.textContent).not.toContain('Khung ứng dụng đã sẵn sàng');
  });
});
