import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ST20ProgressService } from '../data-access/st20-progress.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentAchievement } from '../../shared/models/student-api.models';

@Component({
  imports: [DatePipe, RouterLink],
  selector: 'study-st20-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-community.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st20-page.html',
})
export class ST20Page implements OnInit {
  private readonly data = inject(ST20ProgressService);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly achievements = signal<StudentAchievement[]>([]);

  ngOnInit(): void {
    this.data.achievements().subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else this.achievements.set(response.data.items);
        this.loading.set(false);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.loading.set(false);
      },
    });
  }
}
