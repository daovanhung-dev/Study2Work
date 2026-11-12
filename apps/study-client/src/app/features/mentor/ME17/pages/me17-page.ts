import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { Me17StudentProgressService } from '../data-access/me17-student-progress.service';
import {
  type StudentCourseProgressDto,
  parsePositiveInt64,
} from '../models/me17-student-progress.models';
import { Me17LessonList } from '../ui/me17-lesson-list';
import { Me17StudentSummary } from '../ui/me17-student-summary';

export type Me17ScreenState =
  | 'invalid-param'
  | 'loading'
  | 'ready'
  | 'unauthorized'
  | 'forbidden'
  | 'not-found'
  | 'error';

@Component({
  imports: [RouterLink, Me17StudentSummary, Me17LessonList],
  selector: 'study-me17-page',
  styleUrl: './me17-page.css',
  templateUrl: './me17-page.html',
})
export class ME17Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly studentProgressService = inject(Me17StudentProgressService);

  readonly courseId = signal<number | null>(null);
  readonly studentId = signal<number | null>(null);
  readonly screenState = signal<Me17ScreenState>('loading');
  readonly errorMessage = signal<string>('');
  readonly traceId = signal<string>('');

  readonly progressData = signal<StudentCourseProgressDto | null>(null);

  ngOnInit(): void {
    const paramMap = this.route.snapshot.paramMap;
    const parsedCourseId = parsePositiveInt64(paramMap.get('courseId'));
    const parsedStudentId = parsePositiveInt64(paramMap.get('studentId'));

    if (parsedCourseId === null || parsedStudentId === null) {
      this.courseId.set(parsedCourseId);
      this.studentId.set(parsedStudentId);
      this.screenState.set('invalid-param');
      this.errorMessage.set(
        'Mã khóa học (`courseId`) hoặc mã học viên (`studentId`) không phải số nguyên dương int64 hợp lệ.',
      );
      return;
    }

    this.courseId.set(parsedCourseId);
    this.studentId.set(parsedStudentId);
    this.loadStudentProgress(parsedCourseId, parsedStudentId);
  }

  reload(): void {
    const cid = this.courseId();
    const sid = this.studentId();
    if (cid !== null && sid !== null) {
      this.loadStudentProgress(cid, sid);
    }
  }

  backToCourseProgress(): void {
    const cid = this.courseId();
    if (cid !== null) {
      void this.router.navigate(['/mentor/courses', cid, 'progress']);
    }
  }

  private loadStudentProgress(courseId: number, studentId: number): void {
    this.screenState.set('loading');
    this.errorMessage.set('');
    this.traceId.set('');

    this.studentProgressService.getStudentCourseProgress(courseId, studentId).subscribe({
      next: (envelope) => {
        this.progressData.set(envelope.data);
        this.traceId.set(envelope.traceId ?? '');
        this.screenState.set('ready');
      },
      error: (err: unknown) => {
        this.progressData.set(null);
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
            this.errorMessage.set(
              'Bạn không có quyền xem tiến độ của học viên trong khóa học này (403).',
            );
            return;
          }
          if (err.status === 404) {
            this.screenState.set('not-found');
            this.errorMessage.set(
              'Không tìm thấy khóa học hoặc học viên không thuộc danh sách lớp đang hoạt động (404).',
            );
            return;
          }
          this.errorMessage.set(body?.message ?? 'Không thể tải tiến độ chi tiết của học viên.');
        } else {
          this.errorMessage.set('Lỗi kết nối tới máy chủ Study API.');
        }
        this.screenState.set('error');
      },
    });
  }
}
