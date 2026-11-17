import { toSignal } from '@angular/core/rxjs-interop';
import { computed } from '@angular/core';
import { StudentLessonAccessService } from '../data-access/ST-10-lesson-access.service';
import type { StudentLessonAccessState } from '../models/ST-10-lesson-access.models';
import { ActivatedRoute } from '@angular/router';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
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
  private readonly params = toSignal(this.route.paramMap, {
    initialValue: this.route.snapshot.paramMap,
  });
  readonly state = computed<StudentLessonAccessState>(() =>
    this.params().get('lessonId')?.trim()
      ? {
          kind: this.source.status,
          title: 'Đang chờ xác minh quyền bài học',
          message:
            'Hệ thống chưa thể thực hiện kiểm tra quyền bài học. Môi trường bài học được cô lập hoàn toàn, không tải trước tài nguyên đa phương tiện, scripts kiểm tra hoặc video chunks.',
        }
      : {
          kind: 'missing-context',
          title: 'Thiếu thông tin trên đường dẫn',
          message: 'Vui lòng mở lại màn hình từ chức năng trước đó.',
        },
  );
}
