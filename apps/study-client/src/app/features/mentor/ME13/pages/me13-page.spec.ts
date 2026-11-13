import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, Router } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';
import { Me13RecipientsService } from '../data-access/me13-recipients.service';
import { MentorCourseItemDto, StudentSummaryDto } from '../models/me13-recipients.models';
import { ME13Page } from './me13-page';

const MOCK_COURSES: MentorCourseItemDto[] = [
  {
    id: 101,
    title: 'Nhập môn Khoa học Dữ liệu',
    category: 'Data Science',
    price: 0,
    status: 'PUBLISHED',
    created_at: '2026-11-01T00:00:00Z',
  },
];

const MOCK_STUDENTS: StudentSummaryDto[] = [
  { id: 501, full_name: 'Nguyễn Văn An', avatar_url: null },
  { id: 502, full_name: 'Trần Thị Bình', avatar_url: null },
];

describe('ME13Page', () => {
  function setup(queryParams: Record<string, string> = {}) {
    const serviceMock: Pick<Me13RecipientsService, 'getMentorCourses' | 'getCourseStudents'> = {
      getMentorCourses: vi.fn().mockReturnValue(of(MOCK_COURSES)),
      getCourseStudents: vi.fn().mockReturnValue(of(MOCK_STUDENTS)),
    };

    TestBed.configureTestingModule({
      imports: [ME13Page],
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
        { provide: Me13RecipientsService, useValue: serviceMock },
      ],
    });

    const fixture: ComponentFixture<ME13Page> = TestBed.createComponent(ME13Page);
    const router = TestBed.inject(Router);
    return { fixture, component: fixture.componentInstance, service: serviceMock, router };
  }

  it('loads mentor courses (#46) and course students (#62) on init', () => {
    const { fixture, component, service } = setup();
    fixture.detectChanges();

    expect(service.getMentorCourses).toHaveBeenCalled();
    expect(service.getCourseStudents).toHaveBeenCalledWith(101);
    expect(component.students().length).toBe(2);

    const rows = (fixture.nativeElement as HTMLElement).querySelectorAll('[data-testid="student-row"]');
    expect(rows.length).toBe(2);
  });

  it('allows selecting recipients and navigating to ME-14 with queryParams and state', () => {
    const { fixture, component, router } = setup();
    const navSpy = vi.spyOn(router, 'navigate').mockResolvedValue(true);
    fixture.detectChanges();

    component.onToggleStudent(501);
    fixture.detectChanges();

    expect(component.selectedIds().has(501)).toBe(true);
    component.proceedToCompose();

    expect(navSpy).toHaveBeenCalledWith(['/mentor/notifications/create'], {
      queryParams: {
        courseId: 101,
        recipients: '501',
      },
      state: {
        courseId: 101,
        recipients: [{ id: 501, full_name: 'Nguyễn Văn An', avatar_url: null }],
      },
    });
  });

  it('restores preselected recipients from queryParams when returning from ME-14', () => {
    const { fixture, component } = setup({ courseId: '101', recipients: '501,502' });
    fixture.detectChanges();

    expect(component.selectedIds().size).toBe(2);
    expect(component.selectedIds().has(501)).toBe(true);
    expect(component.selectedIds().has(502)).toBe(true);
  });
});
