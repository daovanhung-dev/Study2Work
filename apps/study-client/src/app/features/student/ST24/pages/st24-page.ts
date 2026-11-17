import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { ST24CreateDiscussionService } from '../data-access/st24-create-discussion.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentCourseSummary } from '../../shared/models/student-api.models';
import { toSafeStudyId, toSafeStudyNumber } from '../../shared/models/student-api.models';

@Component({
  imports: [FormsModule, RouterLink],
  selector: 'study-st24-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-community.css',
    './st24-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st24-page.html',
})
export class ST24Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly data = inject(ST24CreateDiscussionService);
  readonly loadingCourses = signal(true);
  readonly creating = signal(false);
  readonly error = signal<string | null>(null);
  readonly refreshError = signal<string | null>(null);
  readonly creationAccepted = signal(false);
  readonly createdId = signal<string | null>(null);
  readonly courses = signal<StudentCourseSummary[]>([]);
  readonly selectedCourseId = signal('');
  title = '';
  content = '';

  ngOnInit(): void {
    this.data.courses().subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else {
          this.courses.set(response.data.items);
          const queryId = toSafeStudyNumber(this.route.snapshot.queryParamMap.get('courseId'));
          if (
            queryId !== null &&
            response.data.items.some((course) => course.course_id === queryId)
          )
            this.selectedCourseId.set(String(queryId));
        }
        this.loadingCourses.set(false);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.loadingCourses.set(false);
      },
    });
  }

  create(): void {
    const courseId = toSafeStudyNumber(this.selectedCourseId());
    const title = this.title.trim();
    const content = this.content.trim();
    if (this.creating() || this.creationAccepted()) return;
    if (courseId === null || !title || !content) {
      this.error.set('Chọn khóa học và nhập tiêu đề cùng nội dung.');
      return;
    }
    this.creating.set(true);
    this.error.set(null);
    this.refreshError.set(null);
    this.data.create(courseId, title, content).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) {
          this.error.set(issue);
          this.creating.set(false);
          return;
        }
        this.creationAccepted.set(true);
        const discussionId = toSafeStudyId(response.data?.id);
        if (discussionId) this.createdId.set(discussionId);
        this.data.refresh(courseId).subscribe({
          next: (refreshed) => {
            const refreshIssue = studentEnvelopeError(refreshed.success, refreshed.message);
            if (refreshIssue) {
              this.refreshError.set(refreshIssue);
              this.creating.set(false);
              return;
            }
            this.creating.set(false);
            void this.router.navigate(['/student/discussions'], { queryParams: { courseId } });
          },
          error: (error: unknown) => {
            this.refreshError.set(studentApiErrorMessage(error));
            this.creating.set(false);
          },
        });
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.creating.set(false);
      },
    });
  }

  backToList(): void {
    const courseId = toSafeStudyNumber(this.selectedCourseId());
    void this.router.navigate(['/student/discussions'], {
      queryParams: courseId ? { courseId } : {},
    });
  }

  createdIdForLink(): string | null {
    return toSafeStudyId(this.createdId());
  }
}
