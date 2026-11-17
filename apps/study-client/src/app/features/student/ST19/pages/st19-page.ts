import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { StudentApiService, type SubmissionRecord } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st19-page',
  styleUrls: ['./st19-page.css', '../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st19-page.html',
})
export class ST19Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(StudentApiService);

  readonly submission = new StudentApiState<SubmissionRecord>();
  submissionId = '';

  ngOnInit(): void {
    this.submissionId = this.route.snapshot.paramMap.get('submissionId') ?? '';
    if (this.submissionId) this.submission.load(this.api.getSubmission(this.submissionId));
  }
}
