import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
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

import { ST17AssignmentService } from '../data-access/st17-assignment.service';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import type { StudentAssignment } from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [RouterLink],
  selector: 'study-st17-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    './st17-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st17-page.html',
})
export class ST17Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST17AssignmentService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly retryAssignment$ = new Subject<void>();
  readonly assignmentId = signal(toSafeStudyId(this.route.snapshot.paramMap.get('assignmentId')));
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly assignment = signal<StudentAssignment | null>(null);

  ngOnInit(): void {
    const assignmentId$ = this.route.paramMap.pipe(
      map((params) => toSafeStudyId(params.get('assignmentId'))),
      distinctUntilChanged(),
      tap((assignmentId) => this.assignmentId.set(assignmentId)),
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
}

interface AssignmentLoad {
  assignmentId: string | null;
  response: ApiEnvelope<StudentAssignment> | null;
  error: unknown | null;
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
