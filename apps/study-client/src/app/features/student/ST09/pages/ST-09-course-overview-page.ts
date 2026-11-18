import { HttpErrorResponse } from '@angular/common/http';
import { toSignal } from '@angular/core/rxjs-interop';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { catchError, map, of, startWith, switchMap, type Observable } from 'rxjs';

import { StudentCourseOverviewService } from '../data-access/ST-09-course-overview.service';
import type { StudentCourseOverviewState } from '../models/ST-09-course-overview.models';
import { StudentCourseOverviewView } from '../ui/ST-09-course-overview-view';

const MAX_COURSE_ID = BigInt(Number.MAX_SAFE_INTEGER);

@Component({
  selector: 'study-student-course-overview-page',
  imports: [StudentCourseOverviewView],
  templateUrl: './ST-09-course-overview-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentCourseOverviewPage {
  private readonly source = inject(StudentCourseOverviewService);
  private readonly route = inject(ActivatedRoute);

  readonly state = toSignal(this.route.paramMap.pipe(
    map((params) => params.get('courseId')),
    switchMap((courseId) => this.loadState(courseId)),
  ), { initialValue: loadingState() });

  private loadState(courseId: string | null): Observable<StudentCourseOverviewState> {
    if (courseId === null || courseId.trim() === '') {
      return of({
        kind: 'missing-context',
        title: 'Thiếu thông tin trên đường dẫn',
        message: 'Vui lòng mở lại màn hình từ chức năng trước đó.',
      });
    }
    if (!isValidCourseId(courseId)) {
      return of({
        kind: 'missing-context',
        title: 'Mã khóa học không hợp lệ.',
        message: 'Vui lòng mở lại màn hình từ danh sách khóa học của tôi.',
      });
    }
    return this.source.getOverview(courseId).pipe(
      map((data): StudentCourseOverviewState => data
        ? { kind: 'ready', data }
        : {
            kind: 'not-enrolled',
            title: 'Bạn chưa ghi danh khóa học này.',
            message: 'Danh sách khóa học của bạn không có ghi danh đang hoạt động cho mã khóa học trên đường dẫn.',
          }),
      startWith(loadingState()),
      catchError((error: unknown) => of({
        kind: 'blocked' as const,
        title: 'Chưa thể tải tổng quan khóa học.',
        message: errorMessage(error),
      })),
    );
  }
}

function loadingState(): StudentCourseOverviewState {
  return {
    kind: 'loading',
    title: 'Đang xác minh quyền học...',
    message: 'Vui lòng đợi trong khi hệ thống kiểm tra khóa học của bạn.',
  };
}

function errorMessage(error: unknown): string {
  if (error instanceof HttpErrorResponse) {
    return error.status ? 'Máy chủ trả HTTP ' + error.status + '. Vui lòng thử lại sau.' : 'Không kết nối được máy chủ. Vui lòng thử lại sau.';
  }
  return 'Không đọc được dữ liệu khóa học hợp lệ. Vui lòng thử lại sau.';
}

function isValidCourseId(value: string): boolean {
  return /^[1-9]\d*$/.test(value) && BigInt(value) <= MAX_COURSE_ID;
}
