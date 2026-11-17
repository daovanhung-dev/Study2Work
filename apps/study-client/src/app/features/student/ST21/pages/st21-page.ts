import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { StudentApiService } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st21-page',
  styleUrls: ['../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st21-page.html',
})
export class ST21Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(StudentApiService);
  readonly progress = new StudentApiState<Record<string, unknown>>();
  courseId = '';

  ngOnInit(): void {
    this.courseId = this.route.snapshot.paramMap.get('courseId') ?? '';
    if (this.courseId) this.progress.load(this.api.getCourseProgress(this.courseId));
  }
}
