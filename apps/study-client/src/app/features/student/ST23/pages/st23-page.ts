import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ST23DiscussionsService } from '../data-access/st23-discussions.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentDiscussion, StudentPagination } from '../../shared/models/student-api.models';
import { toSafeStudyId, toSafeStudyNumber } from '../../shared/models/student-api.models';

@Component({
  imports: [FormsModule, RouterLink],
  selector: 'study-st23-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-community.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st23-page.html',
})
export class ST23Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST23DiscussionsService);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly discussions = signal<StudentDiscussion[]>([]);
  readonly pagination = signal<StudentPagination | null>(null);
  readonly courseFilter = signal<number | null>(null);
  readonly page = signal(1);
  courseIdInput = '';

  ngOnInit(): void {
    const queryCourseId = this.route.snapshot.queryParamMap.get('courseId');
    if (queryCourseId) {
      const courseId = toSafeStudyNumber(queryCourseId);
      if (courseId === null) this.error.set('Mã khóa học trong đường dẫn không hợp lệ.');
      else {
        this.courseIdInput = queryCourseId;
        this.courseFilter.set(courseId);
      }
    }
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.error.set(null);
    this.data.discussions(this.courseFilter(), this.page()).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else {
          this.discussions.set(response.data.items);
          this.pagination.set(response.data.pagination);
        }
        this.loading.set(false);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.loading.set(false);
      },
    });
  }

  applyCourseFilter(): void {
    const raw = this.courseIdInput.trim();
    const courseId = raw ? toSafeStudyNumber(raw) : null;
    if (raw && courseId === null) {
      this.error.set('Mã khóa học phải là số nguyên dương an toàn.');
      return;
    }
    this.courseFilter.set(courseId);
    this.page.set(1);
    this.load();
  }

  changePage(delta: number): void {
    const page = this.page() + delta;
    const totalPages = this.pagination()?.total_pages ?? 0;
    if (page < 1 || page > totalPages) return;
    this.page.set(page);
    this.load();
  }

  safeId(id: unknown): string | null {
    return toSafeStudyId(id);
  }
}
