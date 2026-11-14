import { toSignal } from '@angular/core/rxjs-interop';
import { computed } from '@angular/core';
import { StudentCourseOverviewService } from '../data-access/ST-09-course-overview.service';
import type { StudentCourseOverviewState } from '../models/ST-09-course-overview.models';
import { ActivatedRoute } from '@angular/router';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { StudentCourseOverviewView } from '../ui/ST-09-course-overview-view';

@Component({
  selector: 'study-student-course-overview-page',
  imports: [StudentCourseOverviewView],
  templateUrl: './ST-09-course-overview-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentCourseOverviewPage {
  private readonly source = inject(StudentCourseOverviewService);
  private readonly route = inject(ActivatedRoute);
  private readonly params = toSignal(this.route.paramMap, {
    initialValue: this.route.snapshot.paramMap,
  });
  readonly state = computed<StudentCourseOverviewState>(() =>
    this.params().get('courseId')?.trim()
      ? {
          kind: this.source.status,
          title: 'Khóa học chưa sẵn sàng nạp cây nội dung học tập',
          message: 'Đề cương và tiến độ chỉ hiển thị khi quyền học được xác minh.',
        }
      : {
          kind: 'missing-context',
          title: 'Thiếu thông tin trên đường dẫn',
          message: 'Vui lòng mở lại màn hình từ chức năng trước đó.',
        },
  );
}
