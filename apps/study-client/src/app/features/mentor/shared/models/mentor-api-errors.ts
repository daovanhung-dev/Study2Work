import { HttpErrorResponse } from '@angular/common/http';

import { MentorSessionError } from '../../../../core/auth/mentor-session.service';

export function mentorApiErrorMessage(error: unknown): string {
  if (error instanceof MentorSessionError) {
    return error.code === 'LOGIN_REQUIRED'
      ? 'Phiên Mentor không còn hiệu lực. Đăng nhập lại để tiếp tục.'
      : 'Không thể xác nhận phiên Mentor.';
  }
  if (error instanceof HttpErrorResponse) {
    const body = error.error as { message?: unknown } | null;
    if (typeof body?.message === 'string' && body.message.trim()) return body.message;
    if (error.status === 401) return 'Phiên đăng nhập không còn hiệu lực. Đăng nhập lại để tiếp tục.';
    if (error.status === 403) return 'Tài khoản hiện tại không có quyền truy cập dữ liệu này.';
    if (error.status === 404) return 'Không tìm thấy dữ liệu theo đường dẫn này.';
    if (error.status === 422) return 'Thông tin gửi lên chưa hợp lệ.';
    if (error.status === 0) return 'Không thể kết nối tới Study Server.';
  }
  return 'Không thể tải dữ liệu lúc này. Vui lòng thử lại.';
}

export function mentorEnvelopeError(success: boolean, message: string): string | null {
  return success ? null : message || 'Study Server không xác nhận yêu cầu.';
}
