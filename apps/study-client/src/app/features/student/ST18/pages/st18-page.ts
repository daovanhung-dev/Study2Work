import { DatePipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import {
  Subject,
  catchError,
  combineLatest,
  distinctUntilChanged,
  map,
  of,
  startWith,
  switchMap,
  tap,
} from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ST18SubmissionService } from '../data-access/st18-submission.service';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import type {
  StudentAssignment,
  StudentSubmission,
  StudentUploadAsset,
} from '../../shared/models/student-api.models';
import { toSafeStudyId, toSafeStudyNumber } from '../../shared/models/student-api.models';

@Component({
  imports: [DatePipe, FormsModule, RouterLink],
  selector: 'study-st18-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    './st18-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st18-page.html',
})
export class ST18Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly data = inject(ST18SubmissionService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly retryAssignment$ = new Subject<void>();
  readonly assignmentId = signal(toSafeStudyId(this.route.snapshot.paramMap.get('assignmentId')));
  readonly assignment = signal<StudentAssignment | null>(null);
  readonly loading = signal(true);
  readonly busy = signal(false);
  readonly error = signal<string | null>(null);
  readonly content = signal('');
  readonly file = signal<File | null>(null);
  readonly uploadedAsset = signal<StudentUploadAsset | null>(null);
  readonly outcomeUnknownAssignmentId = signal<string | null>(null);
  readonly createdSubmission = signal<CreatedSubmission | null>(null);

  ngOnInit(): void {
    const assignmentId$ = this.route.paramMap.pipe(
      map((params) => toSafeStudyId(params.get('assignmentId'))),
      distinctUntilChanged(),
      tap((assignmentId) => {
        if (this.assignmentId() === assignmentId) return;
        this.assignmentId.set(assignmentId);
        this.assignment.set(null);
        this.error.set(null);
        this.content.set('');
        this.file.set(null);
        this.uploadedAsset.set(null);
      }),
    );

    combineLatest([assignmentId$, this.retryAssignment$.pipe(startWith(undefined))])
      .pipe(
        tap(() => {
          this.loading.set(true);
          this.error.set(null);
          this.assignment.set(null);
        }),
        switchMap(([assignmentId]) => this.loadAssignment(assignmentId)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyAssignment(result));
  }

  retryAssignment(): void {
    this.retryAssignment$.next();
  }

  selectFile(event: Event): void {
    const input = event.target;
    if (!(input instanceof HTMLInputElement)) return;
    this.file.set(input.files?.[0] ?? null);
    this.uploadedAsset.set(null);
  }

  fileSize(bytes: number): string {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  }

  submit(): void {
    const assignment = this.assignment();
    const assignmentId = this.assignmentId();
    if (!assignment || !assignmentId || this.busy()) return;
    if (
      this.outcomeUnknownAssignmentId() === assignmentId ||
      this.createdSubmission()?.assignmentId === assignmentId
    ) {
      return;
    }

    const content = this.content().trim();
    const file = this.file();
    const uploadedAsset = this.uploadedAsset();
    if (!content && !file && !uploadedAsset) {
      this.error.set('Nhập nội dung hoặc đính kèm một tệp trước khi nộp.');
      return;
    }
    this.error.set(null);
    this.busy.set(true);

    const existingUploadId = toSafeStudyNumber(uploadedAsset?.id);
    if (existingUploadId) {
      this.createSubmission(assignmentId, content, existingUploadId);
      return;
    }
    if (!file) {
      this.createSubmission(assignmentId, content, null);
      return;
    }

    this.data.upload(file, assignment.course_id).subscribe({
      next: (response) => {
        const uploadId = toSafeStudyNumber(response.data?.id);
        if (!response.success) {
          this.setErrorFor(assignmentId, 'Chưa thể tải tệp lên. Vui lòng thử lại.');
          this.busy.set(false);
          return;
        }
        if (
          response.businessCode !== 'DESIGN_RESOURCE_CREATED' ||
          !uploadId ||
          !isStudentUploadAsset(response.data)
        ) {
          this.outcomeUnknownAssignmentId.set(assignmentId);
          this.setErrorFor(assignmentId, 'Upload chưa trả về xác nhận hợp lệ; không gửi lại để tránh tải trùng.');
          this.busy.set(false);
          return;
        }
        if (this.assignmentId() === assignmentId) this.uploadedAsset.set(response.data);
        this.createSubmission(assignmentId, content, uploadId);
      },
      error: (error: unknown) => {
        if (error instanceof HttpErrorResponse && error.status === 0) {
          this.outcomeUnknownAssignmentId.set(assignmentId);
        }
        this.setErrorFor(assignmentId, studentApiErrorMessage(error));
        this.busy.set(false);
      },
    });
  }

  private loadAssignment(assignmentId: string | null) {
    if (!assignmentId) return of({ assignmentId, response: null, error: null });
    return this.data.assignment(assignmentId).pipe(
      map((response) => ({ assignmentId, response, error: null })),
      catchError((error: unknown) => of({ assignmentId, response: null, error })),
    );
  }

  private applyAssignment(result: AssignmentLoad): void {
    this.loading.set(false);
    if (!result.assignmentId) {
      this.error.set('Không tìm thấy bài tập này.');
      return;
    }
    if (result.error !== null) {
      this.error.set(studentApiErrorMessage(result.error));
      return;
    }

    const response = result.response;
    if (!response?.success) {
      this.error.set('Chưa thể tải đề bài tập. Vui lòng thử lại.');
      return;
    }
    if (
      response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isStudentAssignment(response.data, result.assignmentId)
    ) {
      this.error.set('Thông tin bài tập không khớp. Hãy tải lại trang.');
      return;
    }
    this.assignment.set(response.data);
  }

  private createSubmission(
    assignmentId: string,
    content: string,
    uploadId: number | null,
  ): void {
    this.data.submit(assignmentId, content || null, uploadId).subscribe({
      next: (response) => {
        if (!response.success) {
          this.setErrorFor(assignmentId, 'Chưa thể gửi bài. Vui lòng kiểm tra nội dung và thử lại.');
          this.busy.set(false);
          return;
        }
        const submissionId = toSafeStudyId(response.data?.id);
        if (
          response.businessCode !== 'DESIGN_RESOURCE_CREATED' ||
          !submissionId ||
          !isStudentSubmission(response.data, assignmentId)
        ) {
          this.outcomeUnknownAssignmentId.set(assignmentId);
          this.setErrorFor(assignmentId, 'Chưa thể xác nhận bài đã được gửi. Nút gửi đã khóa để tránh gửi trùng.');
          this.busy.set(false);
          return;
        }

        this.createdSubmission.set({ assignmentId, submissionId });
        this.busy.set(false);
        if (this.destroyRef.destroyed || this.assignmentId() !== assignmentId) return;
        void this.router
          .navigate(['/student/submissions', submissionId])
          .then((navigated) => {
            if (!navigated) this.error.set('Bài đã được nộp. Mở biên nhận bằng liên kết bên dưới.');
          })
          .catch(() => this.error.set('Bài đã được nộp. Mở biên nhận bằng liên kết bên dưới.'));
      },
      error: (error: unknown) => {
        if (error instanceof HttpErrorResponse && error.status === 0) {
          this.outcomeUnknownAssignmentId.set(assignmentId);
        }
        this.setErrorFor(assignmentId, studentApiErrorMessage(error));
        this.busy.set(false);
      },
    });
  }

  private setErrorFor(assignmentId: string, message: string): void {
    if (this.assignmentId() === assignmentId) this.error.set(message);
  }
}

interface AssignmentLoad {
  assignmentId: string | null;
  response: ApiEnvelope<StudentAssignment> | null;
  error: unknown | null;
}

interface CreatedSubmission {
  assignmentId: string;
  submissionId: string;
}

function isStudentAssignment(value: unknown, assignmentId: string): value is StudentAssignment {
  if (typeof value !== 'object' || value === null) return false;
  const assignment = value as Record<string, unknown>;
  return (
    toSafeStudyId(assignment['id']) === assignmentId &&
    toSafeStudyId(assignment['course_id']) !== null &&
    typeof assignment['title'] === 'string' &&
    (assignment['description'] === undefined ||
      assignment['description'] === null ||
      typeof assignment['description'] === 'string') &&
    (assignment['due_at'] === undefined ||
      assignment['due_at'] === null ||
      typeof assignment['due_at'] === 'string') &&
    (typeof assignment['max_score'] === 'number' || typeof assignment['max_score'] === 'string')
  );
}

function isStudentUploadAsset(value: unknown): value is StudentUploadAsset {
  if (typeof value !== 'object' || value === null) return false;
  const asset = value as Record<string, unknown>;
  return (
    toSafeStudyNumber(asset['id']) !== null &&
    typeof asset['name'] === 'string' &&
    typeof asset['url'] === 'string' &&
    typeof asset['content_type'] === 'string' &&
    typeof asset['size_bytes'] === 'number' &&
    asset['status'] === 'UPLOADED'
  );
}

function isStudentSubmission(value: unknown, assignmentId: string): value is StudentSubmission {
  if (typeof value !== 'object' || value === null) return false;
  const submission = value as Record<string, unknown>;
  return (
    toSafeStudyId(submission['id']) !== null &&
    toSafeStudyId(submission['assignment_id']) === assignmentId &&
    toSafeStudyId(submission['user_id']) !== null &&
    (submission['content'] === undefined ||
      submission['content'] === null ||
      typeof submission['content'] === 'string') &&
    Array.isArray(submission['files']) &&
    submission['status'] === 'SUBMITTED' &&
    typeof submission['submitted_at'] === 'string'
  );
}
