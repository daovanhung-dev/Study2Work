import { toSignal } from '@angular/core/rxjs-interop';
import { computed } from '@angular/core';
import { SystemOperationsService } from '../data-access/SH-07-operations.service';
import type { SystemOperationsState } from '../models/SH-07-operations.models';
import { ActivatedRoute } from '@angular/router';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { SystemOperationsView } from '../ui/SH-07-operations-view';

@Component({
  selector: 'study-system-operations-page',
  imports: [SystemOperationsView],
  templateUrl: './SH-07-operations-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SystemOperationsPage {
  private readonly source = inject(SystemOperationsService);
  private readonly route = inject(ActivatedRoute);
  private readonly params = toSignal(this.route.paramMap, {
    initialValue: this.route.snapshot.paramMap,
  });
  readonly state = computed<SystemOperationsState>(() =>
    this.params().get('operationId')?.trim()
      ? {
          kind: this.source.status,
          title: 'Theo dõi tác vụ chưa khả dụng',
          message:
            'Chưa có hợp đồng xác nhận loại Operation ID, quyền sở hữu và vòng đời tác vụ. Trang này không gửi yêu cầu theo dõi hoặc tạo ID giả.',
        }
      : {
          kind: 'missing-context',
          title: 'Thiếu thông tin trên đường dẫn',
          message: 'Vui lòng mở lại màn hình từ chức năng trước đó.',
        },
  );
}
