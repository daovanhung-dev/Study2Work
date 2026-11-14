import { Injectable } from '@angular/core';
import type { NotFoundViewModel } from '../models/SH-06-not-found.models';

/** Read-only error handoff. Do not fetch recommendations or retry a failed resource here. */
@Injectable({ providedIn: 'root' })
export class NotFoundService {
  read(context: unknown): NotFoundViewModel {
    // A failed API call must not become a resource-not-found result.
    if (
      typeof context === 'object' &&
      context !== null &&
      'status' in context &&
      context.status !== 404
    ) {
      return {
        source: 'error',
        statusLabel: 'Không thể tải tài nguyên',
        title: 'Chưa thể mở nội dung được yêu cầu',
        description:
          'Yêu cầu trước đó chưa thành công. Không thể kết luận tài nguyên không tồn tại.',
      };
    }
    const resource =
      typeof context === 'object' &&
      context !== null &&
      'status' in context &&
      context.status === 404;
    return {
      source: resource ? 'resource' : 'route',
      statusLabel: resource ? 'HTTP 404 · Resource Not Found' : '404 · Không tìm thấy trang',
      title: resource ? 'Không tìm thấy tài nguyên yêu cầu' : 'Không tìm thấy trang yêu cầu',
      description:
        'Trang hoặc tài nguyên bạn tìm kiếm không tồn tại. Vui lòng kiểm tra đường dẫn hoặc trở về trang chủ.',
    };
  }
}
