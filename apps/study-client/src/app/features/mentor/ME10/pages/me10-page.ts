import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { Me10GradingService } from '../data-access/me10-grading.service';
import {
  type MutationStatus,
  type SubmissionDetailDto,
  parseStrictInt32Score,
  parseSubmissionIdParam,
} from '../models/me10-grading.models';
import { Me10EvaluationPanel } from '../ui/me10-evaluation-panel';
import { Me10SubmissionPanel } from '../ui/me10-submission-panel';

export type Me10ScreenState =
  | 'invalid-param'
  | 'loading'
  | 'ready'
  | 'unauthorized'
  | 'forbidden'
  | 'not-found'
  | 'error';

@Component({
  imports: [RouterLink, Me10SubmissionPanel, Me10EvaluationPanel],
  selector: 'study-me10-page',
  styleUrl: './me10-page.css',
  templateUrl: './me10-page.html',
})
export class ME10Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly gradingService = inject(Me10GradingService);

  readonly submissionId = signal<number | null>(null);
  readonly screenState = signal<Me10ScreenState>('loading');
  readonly errorMessage = signal<string>('');
  readonly traceId = signal<string>('');
  readonly isStale = signal<boolean>(false);

  readonly submission = signal<SubmissionDetailDto | null>(null);
  readonly refreshingDetail = signal<boolean>(false);

  readonly scoreDraft = signal<string>('');
  readonly feedbackDraft = signal<string>('');

  readonly gradeStatus = signal<MutationStatus>('idle');
  readonly feedbackStatus = signal<MutationStatus>('idle');

  readonly gradeMessage = signal<string>('');
  readonly feedbackMessage = signal<string>('');

  ngOnInit(): void {
    const rawId = this.route.snapshot.paramMap.get('submissionId');
    const parsed = parseSubmissionIdParam(rawId);
    if (parsed === null) {
      this.submissionId.set(null);
      this.screenState.set('invalid-param');
      this.errorMessage.set('Mã bài nộp trên đường dẫn không phải số nguyên dương int64 hợp lệ.');
      return;
    }

    this.submissionId.set(parsed);
    this.loadDetail(parsed, true);
  }

  onScoreInput(value: string): void {
    this.scoreDraft.set(value);
    this.gradeStatus.set('dirty');
    this.gradeMessage.set('');
  }

  onFeedbackInput(value: string): void {
    this.feedbackDraft.set(value);
    this.feedbackStatus.set('dirty');
    this.feedbackMessage.set('');
  }

  refreshSubmission(): void {
    const id = this.submissionId();
    if (id !== null) {
      this.loadDetail(id, false);
    }
  }

  submitGrade(): void {
    const id = this.submissionId();
    if (id === null || this.gradeStatus() === 'saving') {
      return;
    }

    const parsedScore = parseStrictInt32Score(this.scoreDraft());
    if (parsedScore === null) {
      this.gradeStatus.set('error');
      this.gradeMessage.set('Điểm số phải là số nguyên hợp lệ (int32) trước khi gửi API #56.');
      return;
    }

    this.gradeStatus.set('saving');
    this.gradeMessage.set('');

    this.gradingService
      .saveGrade(id, {
        score: parsedScore,
        rubric_items: '[]',
      })
      .subscribe({
        next: (envelope) => {
          if (envelope.data) {
            this.submission.set(envelope.data);
          }
          this.gradeStatus.set('saved');
          this.gradeMessage.set('Đã lưu điểm số thành công qua API #56 (status = GRADED).');
          this.revalidateAfterMutation(id);
        },
        error: (err: unknown) => {
          this.gradeStatus.set('error');
          this.gradeMessage.set(this.extractErrorMessage(err, 'Không thể lưu điểm số qua API #56.'));
        },
      });
  }

  submitFeedback(): void {
    const id = this.submissionId();
    if (id === null || this.feedbackStatus() === 'saving') {
      return;
    }

    this.feedbackStatus.set('saving');
    this.feedbackMessage.set('');

    this.gradingService
      .saveFeedback(id, {
        feedback_text: this.feedbackDraft(),
        attachments: '[]',
      })
      .subscribe({
        next: (envelope) => {
          if (envelope.data) {
            this.submission.set(envelope.data);
          }
          this.feedbackStatus.set('saved');
          this.feedbackMessage.set('Đã gửi nhận xét thành công qua API #57.');
          this.revalidateAfterMutation(id);
        },
        error: (err: unknown) => {
          this.feedbackStatus.set('error');
          this.feedbackMessage.set(
            this.extractErrorMessage(err, 'Không thể gửi nhận xét qua API #57.'),
          );
        },
      });
  }

  backToSubmissionsList(): void {
    void this.router.navigate(['/mentor/submissions']);
  }

  private loadDetail(submissionId: number, initial: boolean): void {
    if (initial) {
      this.screenState.set('loading');
    } else {
      this.refreshingDetail.set(true);
    }
    this.errorMessage.set('');
    this.traceId.set('');

    this.gradingService.getSubmissionDetail(submissionId).subscribe({
      next: (envelope) => {
        this.refreshingDetail.set(false);
        this.isStale.set(false);
        const data = envelope.data;
        this.submission.set(data);
        this.traceId.set(envelope.traceId ?? '');

        if (this.gradeStatus() !== 'dirty') {
          this.scoreDraft.set(
            data?.score !== undefined && data?.score !== null ? String(Math.trunc(Number(data.score))) : '',
          );
        }
        if (this.feedbackStatus() !== 'dirty') {
          this.feedbackDraft.set(data?.feedback ?? '');
        }
        this.screenState.set('ready');
      },
      error: (err: unknown) => {
        this.refreshingDetail.set(false);
        if (!initial && this.submission() !== null) {
          this.isStale.set(true);
          return;
        }
        this.handleLoadError(err);
      },
    });
  }

  private revalidateAfterMutation(submissionId: number): void {
    this.refreshingDetail.set(true);
    this.gradingService.getSubmissionDetail(submissionId).subscribe({
      next: (envelope) => {
        this.refreshingDetail.set(false);
        this.isStale.set(false);
        const data = envelope.data;
        this.submission.set(data);
        if (this.gradeStatus() !== 'dirty' && data?.score !== undefined && data?.score !== null) {
          this.scoreDraft.set(String(Math.trunc(Number(data.score))));
        }
        if (this.feedbackStatus() !== 'dirty' && data?.feedback !== undefined) {
          this.feedbackDraft.set(data.feedback ?? '');
        }
      },
      error: () => {
        this.refreshingDetail.set(false);
        this.isStale.set(true);
      },
    });
  }

  private handleLoadError(err: unknown): void {
    if (err instanceof HttpErrorResponse) {
      const body = err.error as { message?: string; traceId?: string } | null;
      this.traceId.set(body?.traceId ?? '');
      if (err.status === 401) {
        this.screenState.set('unauthorized');
        this.errorMessage.set('Phiên đăng nhập giảng viên chưa xác thực hoặc đã hết hạn (401).');
        return;
      }
      if (err.status === 403) {
        this.screenState.set('forbidden');
        this.errorMessage.set('Bạn không có quyền truy cập bài nộp này (403).');
        return;
      }
      if (err.status === 404) {
        this.screenState.set('not-found');
        this.errorMessage.set('Không tìm thấy bài nộp theo mã đã cung cấp (404).');
        return;
      }
      this.errorMessage.set(body?.message ?? 'Không thể tải chi tiết bài nộp.');
    } else {
      this.errorMessage.set('Lỗi kết nối tới máy chủ Study API.');
    }
    this.screenState.set('error');
  }

  private extractErrorMessage(err: unknown, fallback: string): string {
    if (err instanceof HttpErrorResponse) {
      const body = err.error as {
        message?: string;
        meta?: { fieldErrors?: readonly { field?: string; message?: string }[] };
      } | null;
      const firstFieldErr = body?.meta?.fieldErrors?.[0];
      if (firstFieldErr?.message) {
        return `${body?.message ?? fallback} (${firstFieldErr.field}: ${firstFieldErr.message})`;
      }
      if (body?.message) {
        return body.message;
      }
    }
    return fallback;
  }
}
