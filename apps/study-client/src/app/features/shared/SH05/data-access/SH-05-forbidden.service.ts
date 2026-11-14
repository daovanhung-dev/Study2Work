import { Injectable } from '@angular/core';
import type { AccessFailureViewModel } from '../models/SH-05-forbidden.models';

/** Maps the previous request's handoff; opening SH05 must not reissue /users/me or refresh. */
@Injectable({ providedIn: 'root' })
export class AccessFailureService {
  read(context: unknown): AccessFailureViewModel {
    const value =
      typeof context === 'object' && context !== null ? (context as Record<string, unknown>) : {};
    const status = value['status'] === 401 || value['status'] === 403 ? value['status'] : null;
    const trace = value['traceId'];
    return {
      status,
      traceId:
        status !== null && typeof trace === 'string' && /^[a-zA-Z0-9._:-]{1,128}$/.test(trace)
          ? trace
          : null,
      title:
        status === 403
          ? 'Không đủ quyền truy cập hệ thống'
          : status === 401
            ? 'Cần đăng nhập lại'
            : 'Chưa thể mở nội dung được bảo vệ',
      description:
        status === 403
          ? 'Tài khoản không có quyền truy cập nội dung được yêu cầu.'
          : status === 401
            ? 'Yêu cầu trước đó không được xác thực. Vui lòng đăng nhập lại.'
            : 'Trang này chưa nhận được kết quả xác thực từ một yêu cầu được bảo vệ. Vui lòng đăng nhập rồi mở lại nội dung cần xem.',
    };
  }
}
