import { toSignal } from '@angular/core/rxjs-interop';
import { computed } from '@angular/core';
import { StudentPaymentService } from '../data-access/ST-06-payment.service';
import type { StudentPaymentState } from '../models/ST-06-payment.models';
import { ActivatedRoute } from '@angular/router';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { StudentPaymentView } from '../ui/ST-06-payment-view';

const MAX_ORDER_ID = 9_223_372_036_854_775_807n;

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

  readonly state = computed<StudentPaymentState>(() => {
    const orderId = this.params().get('orderId');
    if (!isValidOrderId(orderId)) {
      return {
        kind: 'missing-context',
        title: 'Mã đơn hàng không hợp lệ.',
        message: 'Vui lòng mở lại màn hình từ luồng ghi danh.',
      };
    }
    return {
      kind: this.source.status,
      title: 'Chưa có thông tin thanh toán để hiển thị.',
      message: 'Cổng thanh toán hiện chưa được cấu hình. Chưa thể khởi tạo hoặc xác nhận giao dịch cho mã đơn trên đường dẫn.',
    };
  });
}

function isValidOrderId(value: string | null): boolean {
  return value !== null && /^[1-9]\d*$/.test(value) && BigInt(value) <= MAX_ORDER_ID;
}
