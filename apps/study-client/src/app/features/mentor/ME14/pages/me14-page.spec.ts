import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, Router } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';
import { Me14CreateNotificationService } from '../data-access/me14-create-notification.service';
import { CourseContentSummaryDto } from '../models/me14-create-notification.models';
import { ME14Page } from './me14-page';

const MOCK_CONTENTS: CourseContentSummaryDto[] = [
  {
    id: 10,
    course_id: 101,
    title: 'Bài 1: Giới thiệu khóa học',
    content_type: 'VIDEO',
    order: 1,
  },
];

describe('ME14Page', () => {
  function setup(queryParams: Record<string, string> = { courseId: '101', recipients: '501,502' }) {
    const serviceMock: Pick<
      Me14CreateNotificationService,
      'getCourseContents' | 'createNotification'
    > = {
      getCourseContents: vi.fn().mockReturnValue(of(MOCK_CONTENTS)),
      createNotification: vi.fn().mockReturnValue(
        of({
          operation: { operation_id: 'notif-op-900', status: 'QUEUED' },
          notificationIds: [900, 901],
        }),
      ),
    };

    TestBed.configureTestingModule({
      imports: [ME14Page],
      providers: [
        provideRouter([]),
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              queryParamMap: convertToParamMap(queryParams),
            },
          },
        },
        { provide: Me14CreateNotificationService, useValue: serviceMock },
      ],
    });

    const fixture: ComponentFixture<ME14Page> = TestBed.createComponent(ME14Page);
    const router = TestBed.inject(Router);
    return { fixture, component: fixture.componentInstance, service: serviceMock, router };
  }

  it('loads course contents (#49) and parses recipients CSV on init', () => {
    const { fixture, component, service } = setup();
    fixture.detectChanges();

    expect(service.getCourseContents).toHaveBeenCalledWith(101);
    expect(component.parsedRecipients().validIds).toEqual([501, 502]);
    expect(component.contentIdInput()).toBe('10');
  });

  it('submits notification payload (#63) and navigates to ME-15 with notification IDs', () => {
    const { fixture, component, service, router } = setup();
    const navSpy = vi.spyOn(router, 'navigate').mockResolvedValue(true);
    fixture.detectChanges();

    component.title.set('Nhắc nhở hoàn thành Bài 1');
    component.onToggleChannel('EMAIL');
    fixture.detectChanges();

    expect(component.canSubmit()).toBe(true);
    component.submitNotification();

    expect(service.createNotification).toHaveBeenCalledWith({
      recipients: '501,502',
      title: 'Nhắc nhở hoàn thành Bài 1',
      content: 10,
      channels: 'PUSH,EMAIL',
    });

    expect(navSpy).toHaveBeenCalledWith(['/mentor/notifications/status'], {
      queryParams: {
        ids: '900,901',
        op: 'notif-op-900',
        courseId: 101,
      },
      state: {
        operation: { operation_id: 'notif-op-900', status: 'QUEUED' },
        notificationIds: [900, 901],
        courseId: 101,
        title: 'Nhắc nhở hoàn thành Bài 1',
      },
    });
  });

  it('blocks submit when recipients CSV contains invalid tokens', () => {
    const { fixture, component } = setup({ courseId: '101', recipients: '501,abc' });
    fixture.detectChanges();

    component.title.set('Thông báo kiểm tra');
    fixture.detectChanges();

    expect(component.parsedRecipients().invalidTokens).toEqual(['abc']);
    expect(component.canSubmit()).toBe(false);
  });
});
