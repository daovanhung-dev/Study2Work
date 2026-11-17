import { Component, OnInit, inject } from '@angular/core';
import { Router } from '@angular/router';

import { StudentApiService, type DiscussionRecord, type StudentPage } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st24-page',
  styleUrls: ['./st24-page.css', '../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st24-page.html',
})
export class ST24Page implements OnInit {
  private readonly api = inject(StudentApiService);
  private readonly router = inject(Router);
  readonly createState = new StudentApiState<DiscussionRecord>();
  readonly discussions = new StudentApiState<StudentPage<DiscussionRecord>>();
  courseId = '';
  title = '';
  content = '';

  ngOnInit(): void {
    this.discussions.load(this.api.getDiscussions());
  }

  createDiscussion(): void {
    const courseId = this.courseId.trim();
    if (!/^-?\d+$/.test(courseId) || !this.title.trim() || !this.content.trim() || this.createState.status() === 'loading') return;
    this.createState.load(this.api.createDiscussion({ course_id: courseId, title: this.title.trim(), content: this.content.trim() }), (discussion) => {
      if (discussion?.id !== undefined && discussion?.id !== null) {
        void this.router.navigate(['/student/discussions', discussion.id]);
      } else {
        this.discussions.load(this.api.getDiscussions({ courseId }));
      }
    });
  }
}
