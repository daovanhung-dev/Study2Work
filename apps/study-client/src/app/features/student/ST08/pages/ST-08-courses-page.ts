import { StudentCoursesService } from '../data-access/ST-08-courses.service';
import type { StudentCoursesState } from '../models/ST-08-courses.models';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { StudentCoursesView } from '../ui/ST-08-courses-view';

@Component({
  selector: 'study-student-courses-page',
  imports: [StudentCoursesView],
  templateUrl: './ST-08-courses-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentCoursesPage {
  private readonly source = inject(StudentCoursesService);

  readonly state: StudentCoursesState = {
    kind: this.source.status,
    title: 'Chưa thể tải khóa học của bạn.',
    message:
      'Danh sách ghi danh và tiến độ chưa có hợp đồng dữ liệu chạy được. Chúng tôi chưa thể xác nhận bạn đã ghi danh hay chưa.',
  };
}
