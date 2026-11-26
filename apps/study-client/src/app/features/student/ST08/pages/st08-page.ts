import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ST08CoursesService } from '../data-access/st08-courses.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import {
  hasStudentCoursePageCountMismatch,
  isStudentCoursePage,
} from '../../shared/models/student-course-page.guard';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentCourseSummary, StudentPagination } from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';
import { StudentPublicFrame } from '../../../../shared/ui/student-public-frame';

@Component({
  imports: [DatePipe, RouterLink, StudentPublicFrame],
  selector: 'study-st08-page',
  styleUrls: ['./st08-page.css', '../../shared/ui/student-api-page.css'],
  templateUrl: './st08-page.html',
})
export class ST08Page implements OnInit {
  private readonly data = inject(ST08CoursesService);
  private loadGeneration = 0;
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly courses = signal<StudentCourseSummary[]>([]);
  readonly pagination = signal<StudentPagination | null>(null);
  readonly page = signal(1);
  readonly filter = signal<'all' | 'active' | 'completed'>('all');
  readonly snapshotMismatch = signal(false);

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.error.set(null);
    this.snapshotMismatch.set(false);
    this.courses.set([]);
    this.pagination.set(null);
    const requestedPage = this.page();
    const requestedFilter = this.filter();
    const statusParam =
      requestedFilter === 'active'
        ? 'ACTIVE'
        : requestedFilter === 'completed'
          ? 'COMPLETED'
          : undefined;
    const generation = ++this.loadGeneration;
    this.data.courses(requestedPage, statusParam).subscribe({
      next: (response) => {
        if (generation !== this.loadGeneration) return;
        const issue = envelopeIssue(response);
        if (issue) this.error.set(issue);
        else if (response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
          this.error.set('Chưa thể tải khóa học. Vui lòng thử lại.');
        } else if (!isStudentCoursePage(response.data, requestedPage, statusParam)) {
          this.error.set('Danh sách khóa học chưa đúng định dạng. Hãy tải lại trang.');
        } else {
          const lastAvailablePage = Math.max(response.data.pagination.total_pages, 1);
          if (requestedPage > lastAvailablePage) {
            this.page.set(lastAvailablePage);
            this.load();
            return;
          }
          this.snapshotMismatch.set(hasStudentCoursePageCountMismatch(response.data));
          this.courses.set(response.data.items);
          this.pagination.set(response.data.pagination);
        }
        this.loading.set(false);
      },
      error: (error: unknown) => {
        if (generation !== this.loadGeneration) return;
        this.error.set(studentApiErrorMessage(error));
        this.loading.set(false);
      },
    });
  }

  changePage(delta: number): void {
    const nextPage = this.page() + delta;
    const totalPages = this.pagination()?.total_pages ?? 0;
    if (this.snapshotMismatch() || nextPage < 1 || nextPage > totalPages) return;
    this.page.set(nextPage);
    this.load();
  }

  changeFilter(filter: 'all' | 'active' | 'completed'): void {
    if (this.filter() === filter) return;
    this.filter.set(filter);
    this.page.set(1);
    this.load();
  }

  safeCourseId(courseId: number): string | null {
    return toSafeStudyId(courseId);
  }

  enrollmentStatusLabel(status: string): string {
    const normalized = status.trim().toUpperCase();
    if (normalized === 'ACTIVE') return 'Đang học';
    if (normalized === 'COMPLETED') return 'Đã hoàn thành';
    if (normalized === 'CANCELLED') return 'Đã hủy';
    return 'Trạng thái đang được xác nhận';
  }

  courseStatusLabel(status: string | null | undefined): string {
    if (!status) return 'Chưa có dữ liệu';
    return status === 'PUBLISHED' ? 'Đã xuất bản' : 'Chưa hỗ trợ trạng thái này';
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
