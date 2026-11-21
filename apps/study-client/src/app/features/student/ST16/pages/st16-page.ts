import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DatePipe } from '@angular/common';
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

import { ST16ResultService } from '../data-access/st16-result.service';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import type { StudentQuizAttempt } from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [DatePipe, RouterLink],
  selector: 'study-st16-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    './st16-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st16-page.html',
})
export class ST16Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST16ResultService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly retryResult$ = new Subject<void>();
  readonly attemptId = signal(toSafeStudyId(this.route.snapshot.paramMap.get('attemptId')));
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly result = signal<StudentQuizAttempt | null>(null);

  ngOnInit(): void {
    const attemptId$ = this.route.paramMap.pipe(
      map((params) => toSafeStudyId(params.get('attemptId'))),
      distinctUntilChanged(),
      tap((attemptId) => this.attemptId.set(attemptId)),
    );

    combineLatest([attemptId$, this.retryResult$.pipe(startWith(undefined))])
      .pipe(
        tap(() => {
          this.loading.set(true);
          this.error.set(null);
          this.result.set(null);
        }),
        switchMap(([attemptId]) => this.loadResult(attemptId)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyResult(result));
  }

  retryResult(): void {
    this.retryResult$.next();
  }

  isPending(status: string): boolean {
    return status === 'PENDING_GRADE';
  }

  resultStatusLabel(status: string): string {
    if (status === 'PENDING_GRADE') return 'Đang chờ chấm';
    return status === 'GRADED' ? 'Đã chấm' : 'Trạng thái chưa hỗ trợ';
  }

  private loadResult(attemptId: string | null) {
    if (!attemptId) return of({ attemptId, response: null, error: null });
    return this.data.result(attemptId).pipe(
      map((response) => ({ attemptId, response, error: null })),
      catchError((error: unknown) => of({ attemptId, response: null, error })),
    );
  }

  private applyResult(result: ResultLoad): void {
    this.loading.set(false);
    if (!result.attemptId) {
      this.error.set('Không tìm thấy kết quả bài kiểm tra này.');
      return;
    }
    if (result.error !== null) {
      this.error.set(studentApiErrorMessage(result.error));
      return;
    }

    const response = result.response;
    if (!response?.success) {
      this.error.set('Chưa thể tải kết quả bài kiểm tra. Vui lòng thử lại.');
      return;
    }
    if (response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
      this.error.set('Chưa thể tải kết quả bài kiểm tra. Vui lòng thử lại.');
      return;
    }
    if (!isStudentQuizResult(response.data) || toSafeStudyId(response.data.id) !== result.attemptId) {
      this.error.set('Kết quả không khớp với bài kiểm tra này. Hãy tải lại trang.');
      return;
    }
    this.result.set(response.data);
  }
}

interface ResultLoad {
  attemptId: string | null;
  response: ApiEnvelope<StudentQuizAttempt> | null;
  error: unknown | null;
}

function isStudentQuizResult(value: unknown): value is StudentQuizAttempt {
  if (typeof value !== 'object' || value === null) return false;
  const attempt = value as Record<string, unknown>;
  return (
    toSafeStudyId(attempt['id']) !== null &&
    toSafeStudyId(attempt['quiz_id']) !== null &&
    (attempt['status'] === 'PENDING_GRADE' || attempt['status'] === 'GRADED') &&
    typeof attempt['started_at'] === 'string' &&
    (attempt['submitted_at'] === undefined ||
      attempt['submitted_at'] === null ||
      typeof attempt['submitted_at'] === 'string') &&
    (attempt['score'] === undefined ||
      attempt['score'] === null ||
      typeof attempt['score'] === 'string') &&
    (attempt['passed'] === undefined ||
      attempt['passed'] === null ||
      typeof attempt['passed'] === 'boolean') &&
    Array.isArray(attempt['answers']) &&
    attempt['answers'].every((answer: unknown) => {
      if (typeof answer !== 'object' || answer === null) return false;
      return toSafeStudyId((answer as Record<string, unknown>)['question_id']) !== null;
    })
  );
}
