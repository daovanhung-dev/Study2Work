import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { StudentApiService, type QuizAttemptRecord } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st16-page',
  styleUrls: ['./st16-page.css', '../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st16-page.html',
})
export class ST16Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(StudentApiService);

  readonly result = new StudentApiState<QuizAttemptRecord>();
  attemptId = '';

  ngOnInit(): void {
    this.attemptId = this.route.snapshot.paramMap.get('attemptId') ?? '';
    if (this.attemptId) this.result.load(this.api.getAttemptResult(this.attemptId));
  }

  get isGraded(): boolean {
    return this.result.data()?.status === 'GRADED';
  }
}
