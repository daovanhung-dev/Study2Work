import { Component, OnInit, inject } from '@angular/core';

import { StudentApiService, type DiscussionRecord, type StudentPage } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st23-page',
  styleUrls: ['../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st23-page.html',
})
export class ST23Page implements OnInit {
  private readonly api = inject(StudentApiService);
  readonly discussions = new StudentApiState<StudentPage<DiscussionRecord>>();

  ngOnInit(): void {
    this.discussions.load(this.api.getDiscussions());
  }
}
