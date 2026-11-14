import { StudentOverviewService } from '../data-access/ST-01-overview.service';
import type { StudentOverviewState } from '../models/ST-01-overview.models';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { StudentOverviewView } from '../ui/ST-01-overview-view';

@Component({
  selector: 'study-student-overview-page',
  imports: [StudentOverviewView],
  templateUrl: './ST-01-overview-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentOverviewPage {
  private readonly source = inject(StudentOverviewService);

  readonly state: StudentOverviewState = {
    kind: this.source.status,
    title: 'Hợp đồng chờ kích hoạt',
    message: 'Chưa có dữ liệu tổng quan học tập được xác minh.',
  };
}
