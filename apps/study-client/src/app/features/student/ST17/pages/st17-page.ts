import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { StudentApiService, type AssignmentRecord } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st17-page',
  styleUrls: ['./st17-page.css', '../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st17-page.html',
})
export class ST17Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(StudentApiService);

  readonly assignment = new StudentApiState<AssignmentRecord>();
  assignmentId = '';

  ngOnInit(): void {
    this.assignmentId = this.route.snapshot.paramMap.get('assignmentId') ?? '';
    if (this.assignmentId) this.assignment.load(this.api.getAssignment(this.assignmentId));
  }
}
