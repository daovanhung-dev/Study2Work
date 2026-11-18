import { HttpErrorResponse } from '@angular/common/http';
import { toSignal } from '@angular/core/rxjs-interop';
import { StudentLessonAccessService } from '../data-access/ST-10-lesson-access.service';
import type { StudentLessonAccessState } from '../models/ST-10-lesson-access.models';
import { ActivatedRoute } from '@angular/router';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { catchError, map, of, startWith, switchMap, type Observable } from 'rxjs';
import { StudentLessonAccessView } from '../ui/ST-10-lesson-access-view';

@Component({
  selector: 'study-student-lesson-access-page',
  imports: [StudentLessonAccessView],
  templateUrl: './ST-10-lesson-access-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentLessonAccessPage {
  private readonly source = inject(StudentLessonAccessService);
  private readonly route = inject(ActivatedRoute);
  readonly state = toSignal(this.route.paramMap.pipe(
    map((params) => params.get('lessonId')),
    switchMap((lessonId) => this.loadAccess(lessonId)),
  ), { initialValue: checkingState() });

  private loadAccess(lessonId: string | null): Observable<StudentLessonAccessState> {
    if (!lessonId || !/^[1-9]\d*$/.test(lessonId) || !Number.isSafeInteger(Number(lessonId))) {
      return of({ kind: 'missing-context', title: 'Mã bài học không hợp lệ',
        message: 'Vui lòng mở lại màn hình từ danh sách bài học của khóa học.' });
    }
    return this.source.checkAccess(lessonId).pipe(
      map((lesson): StudentLessonAccessState => ({
        kind: 'allowed',
        title: 'Đã xác minh quyền truy cập bài học',
        message: 'Quyền truy cập đã được xác minh. Chức năng bắt đầu học đang chờ hoàn tất hợp đồng API #23 và bàn giao ST-11.',
        lesson,
      })),
      startWith(checkingState()),
      catchError((error: unknown) => of(errorState(error))),
    );
  }
}

function checkingState(): StudentLessonAccessState {
  return { kind: 'checking', title: 'Đang xác minh quyền bài học',
    message: 'Đang gửi yêu cầu kiểm tra quyền tới API #22. Nội dung bài học vẫn được khóa.' };
}

function errorState(error: unknown): StudentLessonAccessState {
  if (error instanceof HttpErrorResponse && error.status === 403) {
    return { kind: 'denied', title: 'Bạn chưa có quyền học bài này',
      message: 'Máy chủ từ chối quyền truy cập bài học. Không tải nội dung hoặc bắt đầu học.' };
  }
  if (error instanceof HttpErrorResponse && error.status === 404) {
    return { kind: 'not-found', title: 'Không tìm thấy bài học',
      message: 'Máy chủ không tìm thấy bài học này. Vui lòng quay lại danh sách khóa học.' };
  }
  return { kind: 'blocked', title: 'Chưa thể xác minh quyền bài học',
    message: 'Không nhận được phản hồi kiểm tra quyền hợp lệ từ máy chủ. Nội dung bài học vẫn được khóa.' };
}
