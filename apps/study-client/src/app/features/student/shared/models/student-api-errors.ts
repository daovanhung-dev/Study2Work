import { HttpErrorResponse } from '@angular/common/http';

export function studentApiErrorMessage(error: unknown): string {
  if (error instanceof HttpErrorResponse) {
    switch (error.status) {
      case 0:
      case 500:
      case 502:
      case 503:
      case 504:
        return 'Không thể kết nối lúc này. Vui lòng thử lại.';
      case 401:
        return 'Phiên đăng nhập không còn hợp lệ. Hãy đăng nhập lại.';
      case 403:
        return 'Bạn không có quyền truy cập nội dung này.';
      case 404:
        return 'Không tìm thấy nội dung hoặc nội dung đã bị gỡ.';
      case 409:
        return 'Trạng thái đã thay đổi. Hãy tải lại để kiểm tra.';
      case 422:
        return 'Thông tin chưa hợp lệ. Hãy kiểm tra lại và thử lần nữa.';
      case 429:
        return 'Bạn đã gửi nhiều yêu cầu trong thời gian ngắn. Hãy chờ một chút rồi thử lại.';
      default:
        return 'Đã xảy ra lỗi. Vui lòng thử lại.';
    }
  }

  return 'Đã xảy ra lỗi. Vui lòng thử lại.';
}

export function studentEnvelopeError(success: boolean, _message: string): string | null {
  return success ? null : 'Yêu cầu chưa được hoàn tất. Vui lòng thử lại.';
}
