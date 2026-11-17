import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ME04LectureCreateService } from '../data-access/me04-lecture-create.service';
import type { MentorCourse } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [RouterLink, MentorPageHeader], selector: 'study-me04-page', styleUrls: ['./me04-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me04-page.html' })
export class ME04Page implements OnInit {
  private readonly data = inject(ME04LectureCreateService);
  private readonly route = inject(ActivatedRoute);
  readonly courseId = signal('');
  readonly courses = signal<MentorCourse[]>([]);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly unsupportedCreate = signal(true);
  ngOnInit(): void {
    this.courseId.set(toSafeMentorId(this.route.snapshot.paramMap.get('courseId')) ?? '');
    this.load();
  }
  load(): void {
    this.loading.set(true); this.error.set(null);
    this.data.courses().subscribe({
      next: (response) => {
        const issue = mentorEnvelopeError(response.success, response.message);
        if (issue) this.error.set(issue);
        else { this.courses.set(response.data.items); if (!this.courseId() && response.data.items[0]) this.courseId.set(toSafeMentorId(response.data.items[0].id) ?? ''); }
        this.loading.set(false);
      }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.loading.set(false); },
    });
  }
  selectCourse(value: string): void { this.courseId.set(toSafeMentorId(value) ?? ''); }
}
