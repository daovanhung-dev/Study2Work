import { Component, OnInit, inject, signal } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ST09CourseOverviewService } from '../data-access/st09-course-overview.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type {
  StudentCourseProgress,
  StudentCourseSummary,
} from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';
import { StudentPublicFrame } from '../../../../shared/ui/student-public-frame';

@Component({
  imports: [RouterLink, StudentPublicFrame],
  selector: 'study-st09-page',
  styleUrls: ['./st09-page.css', '../../shared/ui/student-api-page.css'],
  templateUrl: './st09-page.html',
})
export class ST09Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST09CourseOverviewService);
  readonly courseId = toSafeStudyId(this.route.snapshot.paramMap.get('courseId'));
  readonly enrollmentLoading = signal(true);
  readonly progressLoading = signal(false);
  readonly error = signal<string | null>(null);
  readonly course = signal<StudentCourseSummary | null>(null);
  readonly progress = signal<StudentCourseProgress | null>(null);
  readonly notEnrolled = signal(false);

  ngOnInit(): void {
    if (!this.courseId) {
      this.error.set('Mã khóa học trong đường dẫn không hợp lệ.');
      this.enrollmentLoading.set(false);
      return;
    }
    this.findActiveCourse(1);
  }

  retry(): void {
    if (!this.courseId) return;
    this.error.set(null);
    this.course.set(null);
    this.progress.set(null);
    this.notEnrolled.set(false);
    this.enrollmentLoading.set(true);
    this.findActiveCourse(1);
  }

  progressWidth(): number {
    return Math.max(0, Math.min(100, this.progress()?.progress_percent ?? 0));
  }

  private findActiveCourse(page: number): void {
    this.data.activeCourses(page).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) {
          this.error.set(issue);
          this.enrollmentLoading.set(false);
          return;
        }

        const match = response.data.items.find(
          (item) => toSafeStudyId(item.course_id) === this.courseId,
        );
        if (match) {
          this.course.set(match);
          this.enrollmentLoading.set(false);
          this.loadProgress();
          return;
        }

        if (page < response.data.pagination.total_pages) {
          this.findActiveCourse(page + 1);
          return;
        }

        this.notEnrolled.set(true);
        this.enrollmentLoading.set(false);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.enrollmentLoading.set(false);
      },
    });
  }

  private loadProgress(): void {
    if (!this.courseId) return;
    this.progressLoading.set(true);
    this.data.progress(this.courseId).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else this.progress.set(response.data);
        this.progressLoading.set(false);
      },
      error: (error: unknown) => {
        if (error instanceof HttpErrorResponse && error.status === 404) {
          this.error.set('Study Server không tìm thấy dữ liệu tiến độ cho khóa học này.');
        } else {
          this.error.set(studentApiErrorMessage(error));
        }
        this.progressLoading.set(false);
      },
    });
  }
}
