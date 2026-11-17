import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { ST10LessonAccessService } from '../data-access/st10-lesson-access.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { StudentLesson } from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';
import { StudentPublicFrame } from '../../../../shared/ui/student-public-frame';

@Component({
  imports: [RouterLink, StudentPublicFrame],
  selector: 'study-st10-page',
  styleUrls: ['./st10-page.css', '../../shared/ui/student-api-page.css'],
  templateUrl: './st10-page.html',
})
export class ST10Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly data = inject(ST10LessonAccessService);
  readonly lessonId = toSafeStudyId(this.route.snapshot.paramMap.get('lessonId'));
  readonly accessLoading = signal(true);
  readonly accessError = signal<string | null>(null);
  readonly lesson = signal<StudentLessonPreview | null>(null);
  readonly starting = signal(false);
  readonly started = signal(false);
  readonly startError = signal<string | null>(null);
  readonly canStart = computed(
    () => this.lesson()?.status === 'PUBLISHED' && !this.starting() && !this.started(),
  );

  ngOnInit(): void {
    this.checkAccess();
  }

  checkAccess(): void {
    if (!this.lessonId) {
      this.accessError.set('Mã bài học trong đường dẫn không hợp lệ.');
      this.accessLoading.set(false);
      return;
    }
    this.accessLoading.set(true);
    this.accessError.set(null);
    this.lesson.set(null);
    this.data.access(this.lessonId).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) this.accessError.set(issue);
        else if (toSafeStudyId(response.data.id) !== this.lessonId) {
          this.accessError.set('Study Server trả về mã bài học không khớp.');
        } else {
          this.lesson.set(toLessonPreview(response.data));
        }
        this.accessLoading.set(false);
      },
      error: (error: unknown) => {
        this.accessError.set(studentApiErrorMessage(error));
        this.accessLoading.set(false);
      },
    });
  }

  startLesson(): void {
    if (!this.lessonId || !this.canStart()) return;
    this.starting.set(true);
    this.startError.set(null);
    this.data.start(this.lessonId).subscribe({
      next: (response) => {
        const issue = studentEnvelopeError(response.success, response.message);
        if (issue) {
          this.startError.set(issue);
          this.starting.set(false);
          return;
        }
        if (
          toSafeStudyId(response.data.id) !== this.lessonId ||
          response.data.status !== 'PUBLISHED'
        ) {
          this.startError.set('Study Server chưa xác nhận đúng bài học đã xuất bản.');
          this.starting.set(false);
          return;
        }

        this.started.set(true);
        this.router.navigate(['/student/lessons', this.lessonId]).then((navigated) => {
          this.starting.set(false);
          if (!navigated) {
            this.startError.set('Bài học đã được ghi nhận bắt đầu. Hãy mở ST-11 để tải nội dung.');
          }
        });
      },
      error: (error: unknown) => {
        this.startError.set(studentApiErrorMessage(error));
        this.starting.set(false);
      },
    });
  }
}

interface StudentLessonPreview {
  id: number;
  course_id: number;
  title: string;
  order: number;
  status: string;
}

function toLessonPreview(lesson: StudentLesson): StudentLessonPreview {
  return {
    id: lesson.id,
    course_id: lesson.course_id,
    title: lesson.title,
    order: lesson.order,
    status: lesson.status,
  };
}
