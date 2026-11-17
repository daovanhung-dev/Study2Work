import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ST17AssignmentService } from '../data-access/st17-assignment.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentAssignment } from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [DatePipe, RouterLink],
  selector: 'study-st17-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    './st17-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st17-page.html',
})
export class ST17Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST17AssignmentService);
  readonly assignmentId = toSafeStudyId(this.route.snapshot.paramMap.get('assignmentId'));
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly assignment = signal<StudentAssignment | null>(null);

  ngOnInit(): void {
    if (!this.assignmentId) {
      this.error.set('Mã bài tập không hợp lệ.');
      this.loading.set(false);
      return;
    }
    this.data.assignment(this.assignmentId).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else this.assignment.set(response.data);
        this.loading.set(false);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.loading.set(false);
      },
    });
  }
}
