import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ST22AchievementsService } from '../data-access/st22-achievements.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentAchievement, StudentPagination } from '../../shared/models/student-api.models';

@Component({
  imports: [DatePipe, RouterLink],
  selector: 'study-st22-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-community.css',
    './st22-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st22-page.html',
})
export class ST22Page implements OnInit {
  private readonly data = inject(ST22AchievementsService);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly items = signal<StudentAchievement[]>([]);
  readonly pagination = signal<StudentPagination | null>(null);

  ngOnInit(): void {
    this.data.achievements().subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else {
          this.items.set(response.data.items);
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
}
