import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { StudentApiService, type ApiId, type AssignmentRecord, type SubmissionRecord, type UploadRecord } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st18-page',
  styleUrls: ['./st18-page.css', '../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st18-page.html',
})
export class ST18Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly api = inject(StudentApiService);

  readonly assignment = new StudentApiState<AssignmentRecord>();
  readonly upload = new StudentApiState<UploadRecord>();
  readonly submission = new StudentApiState<SubmissionRecord>();
  assignmentId = '';
  text = '';
  uploadedFiles: UploadRecord[] = [];

  ngOnInit(): void {
    this.assignmentId = this.route.snapshot.paramMap.get('assignmentId') ?? '';
    if (this.assignmentId) this.assignment.load(this.api.getAssignment(this.assignmentId));
  }

  uploadFile(event: Event): void {
    const input = event.currentTarget as HTMLInputElement | null;
    const file = input?.files?.[0];
    const courseId = this.assignment.data()?.course_id;
    if (!file || courseId === undefined || this.upload.status() === 'loading') return;
    this.upload.load(this.api.uploadSubmissionFile(file, courseId), (asset) => {
      if (asset?.id !== undefined && asset?.id !== null) this.uploadedFiles = [...this.uploadedFiles, asset];
      if (input) input.value = '';
    });
  }

  submitAssignment(): void {
    if (!this.assignmentId || this.submission.status() === 'loading') return;
    const fileIds: ApiId[] = this.uploadedFiles.map((file) => file.id);
    this.submission.load(this.api.submitAssignment(this.assignmentId, this.text, fileIds), (submission) => {
      if (submission?.id !== undefined && submission?.id !== null) {
        void this.router.navigate(['/student/submissions', submission.id]);
      }
    });
  }
}
