import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ST08CoursesService } from '../data-access/st08-courses.service';
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
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly courses = signal<StudentCourseSummary[]>([]);
  readonly pagination = signal<StudentPagination | null>(null);
  readonly page = signal(1);

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.error.set(null);
    this.data.courses(this.page()).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else {
          this.courses.set(response.data.items);
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

  changePage(delta: number): void {
    const nextPage = this.page() + delta;
    const totalPages = this.pagination()?.total_pages ?? 0;
    if (nextPage < 1 || nextPage > totalPages) return;
    this.page.set(nextPage);
    this.load();
  }

  safeCourseId(courseId: number): string | null {
    return toSafeStudyId(courseId);
  }
}
