import { toSignal } from '@angular/core/rxjs-interop';
import { computed } from '@angular/core';
import { StudentEnrollResultService } from '../data-access/ST-07-enroll-result.service';
import type { StudentEnrollResultState } from '../models/ST-07-enroll-result.models';
import { ActivatedRoute } from '@angular/router';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { StudentEnrollResultView } from '../ui/ST-07-enroll-result-view';

@Component({
  selector: 'study-student-enroll-result-page',
  imports: [StudentEnrollResultView],
  templateUrl: './ST-07-enroll-result-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentEnrollResultPage {
  private readonly source = inject(StudentEnrollResultService);
  private readonly route = inject(ActivatedRoute);
  private readonly params = toSignal(this.route.paramMap, {
    initialValue: this.route.snapshot.paramMap,
  });
  readonly state = computed<StudentEnrollResultState>(() =>
    this.params().get('courseId')?.trim()
      ? {
          kind: this.source.status,
          title: 'Chưa thể xác nhận kết quả đăng ký.',
          message:
            'Chưa thể truy vấn trạng thái ghi danh hoặc quyền học từ backend. Vui lòng kiểm tra lại sau.',
        }
      : {
          kind: 'missing-context',
          title: 'Thiếu thông tin trên đường dẫn',
          message: 'Vui lòng mở lại màn hình từ chức năng trước đó.',
        },
  );
}
