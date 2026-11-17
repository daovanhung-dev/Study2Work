import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ST01OverviewService } from '../data-access/st01-overview.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentAchievement, StudentCourseSummary } from '../../shared/models/student-api.models';
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
  readonly courses = signal<StudentCourseSummary[]>([]);
  readonly achievementsLoading = signal(true);
  readonly achievementsError = signal<string | null>(null);
  readonly achievements = signal<StudentAchievement[]>([]);

  ngOnInit(): void {
    this.data.activeCourses().subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.coursesError.set(issue);
        else this.courses.set(response.data.items);
        this.coursesLoading.set(false);
      },
      error: (error: unknown) => {
        this.coursesError.set(studentApiErrorMessage(error));
        this.coursesLoading.set(false);
      },
    });

    this.data.achievements().subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.achievementsError.set(issue);
        else this.achievements.set(response.data.items);
        this.achievementsLoading.set(false);
      },
      error: (error: unknown) => {
        this.achievementsError.set(studentApiErrorMessage(error));
        this.achievementsLoading.set(false);
      },
    });
  }

  safeCourseId(courseId: number): string | null {
    return toSafeStudyId(courseId);
  }
}
