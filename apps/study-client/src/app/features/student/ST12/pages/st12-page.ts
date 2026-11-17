import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ST12ResourcesService } from '../data-access/st12-resources.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentLessonResources } from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [RouterLink],
  selector: 'study-st12-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    './st12-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st12-page.html',
})
export class ST12Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST12ResourcesService);
  readonly lessonId = toSafeStudyId(this.route.snapshot.paramMap.get('lessonId'));
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly lesson = signal<StudentLessonResources | null>(null);

  ngOnInit(): void {
    if (!this.lessonId) {
      this.error.set('Mã bài học không hợp lệ.');
      this.loading.set(false);
      return;
    }
    this.data.resources(this.lessonId).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else this.lesson.set(response.data);
        this.loading.set(false);
      },
      error: (error: unknown) => {
        this.error.set(studentApiErrorMessage(error));
        this.loading.set(false);
      },
    });
  }
}
