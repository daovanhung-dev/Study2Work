import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ST21CourseProgressService } from '../data-access/st21-course-progress.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentCourseProgress } from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [RouterLink],
  selector: 'study-st21-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    '../../shared/ui/student-api-community.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st21-page.html',
})
export class ST21Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST21CourseProgressService);
  readonly courseId = toSafeStudyId(this.route.snapshot.paramMap.get('courseId'));
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly progress = signal<StudentCourseProgress | null>(null);

  ngOnInit(): void {
    if (!this.courseId) {
      this.error.set('Mã khóa học không hợp lệ.');
      this.loading.set(false);
      return;
    }
    this.data.progress(this.courseId).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else this.progress.set(response.data);
        this.loading.set(false);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.loading.set(false);
      },
    });
  }

  percentWidth(): number {
    return Math.max(0, Math.min(100, this.progress()?.progress_percent ?? 0));
  }
}
