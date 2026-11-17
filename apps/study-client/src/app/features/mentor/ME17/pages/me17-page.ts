import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ME17StudentProgressService } from '../data-access/me17-student-progress.service';
import type { MentorStudentProgress } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [DatePipe, RouterLink, MentorPageHeader], selector: 'study-me17-page', styleUrls: ['./me17-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me17-page.html' })
export class ME17Page implements OnInit {
  private readonly data = inject(ME17StudentProgressService);
  private readonly route = inject(ActivatedRoute);
  readonly courseId = signal('');
  readonly studentId = signal('');
  readonly progress = signal<MentorStudentProgress | null>(null);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly invalidRoute = signal(false);
  ngOnInit(): void {
    const courseId = toSafeMentorId(this.route.snapshot.paramMap.get('courseId'));
    const studentId = toSafeMentorId(this.route.snapshot.paramMap.get('studentId'));
    if (!courseId || !studentId) { this.invalidRoute.set(true); this.loading.set(false); return; }
    this.courseId.set(courseId); this.studentId.set(studentId); this.load(courseId, studentId);
  }
  load(courseId = this.courseId(), studentId = this.studentId()): void {
    if (!courseId || !studentId) return;
    this.loading.set(true); this.error.set(null);
    this.data.progress(courseId, studentId).subscribe({
      next: (response) => {
        const issue = mentorEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else if (toSafeMentorId(response.data.course_id) !== courseId || toSafeMentorId(response.data.student.id) !== studentId) this.error.set('Response không khớp với course/student trên đường dẫn.');
        else this.progress.set(response.data);
        this.loading.set(false);
      }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.loading.set(false); },
    });
  }
}
