import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { ST01OverviewService } from '../data-access/st01-overview.service';
import {
  hasStudentCoursePageCountMismatch,
  isStudentCoursePage,
} from '../../shared/models/student-course-page.guard';
import { isStudentAchievementPage } from '../../shared/models/student-achievement-page.guard';
import { isStudentNotificationPage } from '../../shared/models/student-notification-page.guard';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type {
  StudentAchievement,
  StudentCourseSummary,
  StudentNotification,
  StudentOverallProgress,
} from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';
import { StudentPublicFrame } from '../../../../shared/ui/student-public-frame';

@Component({
  imports: [DatePipe, RouterLink, StudentPublicFrame],
  selector: 'study-st01-page',
  styleUrls: ['./st01-page.css', '../../shared/ui/student-api-page.css'],
  templateUrl: './st01-page.html',
})
export class ST01Page implements OnInit {
  private readonly data = inject(ST01OverviewService);
  readonly coursesLoading = signal(true);
  readonly coursesError = signal<string | null>(null);
  readonly coursesSnapshotMismatch = signal(false);
  readonly courses = signal<StudentCourseSummary[]>([]);
  readonly progressLoading = signal(true);
  readonly progressError = signal<string | null>(null);
  readonly progress = signal<StudentOverallProgress | null>(null);
  readonly achievementsLoading = signal(true);
  readonly achievementsError = signal<string | null>(null);
  readonly achievementsSnapshotMismatch = signal(false);
  readonly achievements = signal<StudentAchievement[]>([]);
  readonly notificationsLoading = signal(true);
  readonly notificationsError = signal<string | null>(null);
  readonly notificationsSnapshotMismatch = signal(false);
  readonly notifications = signal<StudentNotification[]>([]);
  readonly unreadCount = signal<number | null>(null);

  ngOnInit(): void {
    this.loadCourses();
    this.loadProgress();
    this.loadAchievements();
    this.loadNotifications();
  }

  retryCourses(): void {
    this.loadCourses();
  }

  retryProgress(): void {
    this.loadProgress();
  }

  retryAchievements(): void {
    this.loadAchievements();
  }

  retryNotifications(): void {
    this.loadNotifications();
  }

  safeCourseId(courseId: number): string | null {
    return toSafeStudyId(courseId);
  }

  private loadCourses(): void {
    this.coursesLoading.set(true);
    this.coursesError.set(null);
    this.coursesSnapshotMismatch.set(false);
    this.courses.set([]);
    this.data.activeCourses().subscribe({
      next: (response) => {
        const issue = envelopeIssue(response);
        if (issue) this.coursesError.set(issue);
        else if (response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
          this.coursesError.set('Chưa thể tải khóa học đang học. Vui lòng thử lại.');
        } else if (!isStudentCoursePage(response.data, 1, 'ACTIVE')) {
          this.coursesError.set('Danh sách khóa học chưa đúng định dạng. Hãy tải lại trang.');
        } else {
          this.coursesSnapshotMismatch.set(hasStudentCoursePageCountMismatch(response.data));
          this.courses.set(response.data.items);
        }
        this.coursesLoading.set(false);
      },
      error: (error: unknown) => {
        this.coursesError.set(studentApiErrorMessage(error));
        this.coursesLoading.set(false);
      },
    });
  }

  private loadProgress(): void {
    this.progressLoading.set(true);
    this.progressError.set(null);
    this.progress.set(null);
    this.data.overallProgress().subscribe({
      next: (response) => {
        const issue = envelopeIssue(response);
        if (issue) this.progressError.set(issue);
        else if (
          response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
          typeof response.data?.overall_progress_percent !== 'number'
        ) {
          this.progressError.set('Chưa thể tải tiến độ tổng hợp. Vui lòng thử lại.');
        } else {
          this.progress.set(response.data);
        }
        this.progressLoading.set(false);
      },
      error: (error: unknown) => {
        this.progressError.set(studentApiErrorMessage(error));
        this.progressLoading.set(false);
      },
    });
  }

  private loadAchievements(): void {
    this.achievementsLoading.set(true);
    this.achievementsError.set(null);
    this.achievementsSnapshotMismatch.set(false);
    this.achievements.set([]);
    this.data.achievements().subscribe({
      next: (response) => {
        const issue = envelopeIssue(response);
        if (issue) this.achievementsError.set(issue);
        else if (response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
          this.achievementsError.set('Chưa thể tải thành tích. Vui lòng thử lại.');
        } else if (!isStudentAchievementPage(response.data)) {
          this.achievementsError.set('Danh sách thành tích chưa đúng định dạng. Hãy tải lại trang.');
        } else {
          this.achievementsSnapshotMismatch.set(
            response.data.pagination.total !== response.data.items.length,
          );
          this.achievements.set(response.data.items);
        }
        this.achievementsLoading.set(false);
      },
      error: (error: unknown) => {
        this.achievementsError.set(studentApiErrorMessage(error));
        this.achievementsLoading.set(false);
      },
    });
  }

  private loadNotifications(): void {
    this.notificationsLoading.set(true);
    this.notificationsError.set(null);
    this.notificationsSnapshotMismatch.set(false);
    this.notifications.set([]);
    this.unreadCount.set(null);
    this.data.unreadNotifications().subscribe({
      next: (response) => {
        const issue = envelopeIssue(response);
        if (issue) this.notificationsError.set(issue);
        else if (response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
          this.notificationsError.set('Chưa thể tải thông báo chưa đọc.');
        } else if (!isStudentNotificationPage(response.data, 1, 20, true)) {
          this.notificationsError.set('Danh sách thông báo hiện không hợp lệ.');
        } else {
          const expectedItems = Math.min(
            response.data.pagination.total,
            response.data.pagination.size,
          );
          this.notificationsSnapshotMismatch.set(
            response.data.items.length !== expectedItems,
          );
          this.notifications.set(response.data.items);
          this.unreadCount.set(response.data.pagination.total);
        }
        this.notificationsLoading.set(false);
      },
      error: (error: unknown) => {
        this.notificationsError.set(studentApiErrorMessage(error));
        this.notificationsLoading.set(false);
      },
    });
  }
}

function envelopeIssue(value: unknown): string | null {
  if (
    typeof value !== 'object' ||
    value === null ||
    typeof (value as Record<string, unknown>)['success'] !== 'boolean' ||
    typeof (value as Record<string, unknown>)['message'] !== 'string' ||
    typeof (value as Record<string, unknown>)['businessCode'] !== 'string' ||
    !('data' in value)
  ) {
    return 'Yêu cầu chưa được hoàn tất. Vui lòng thử lại.';
  }
  const response = value as ApiEnvelope<unknown>;
  return studentEnvelopeError(response.success, response.message);
}
