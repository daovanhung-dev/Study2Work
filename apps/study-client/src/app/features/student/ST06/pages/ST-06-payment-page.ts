import { toSignal } from '@angular/core/rxjs-interop';
import { computed } from '@angular/core';
import { StudentPaymentService } from '../data-access/ST-06-payment.service';
import type { StudentPaymentState } from '../models/ST-06-payment.models';
import { ActivatedRoute } from '@angular/router';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { StudentPaymentView } from '../ui/ST-06-payment-view';

@Component({
  selector: 'study-student-payment-page',
  imports: [StudentPaymentView],
  templateUrl: './ST-06-payment-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentPaymentPage {
  private readonly source = inject(StudentPaymentService);
  private readonly route = inject(ActivatedRoute);
  private readonly params = toSignal(this.route.paramMap, {
    initialValue: this.route.snapshot.paramMap,
  });
  readonly state = computed<StudentPaymentState>(() =>
    this.params().get('orderId')?.trim()
      ? {
          kind: this.source.status,
          title: 'Chưa có thông tin thanh toán để hiển thị.',
          message:
            'Chưa thể truy vấn giao dịch hoặc xác nhận trạng thái thanh toán vì hợp đồng API liên quan chưa sẵn sàng.',
        }
      : {
          kind: 'missing-context',
          title: 'Thiếu thông tin trên đường dẫn',
          message: 'Vui lòng mở lại màn hình từ chức năng trước đó.',
        },
  );
}
