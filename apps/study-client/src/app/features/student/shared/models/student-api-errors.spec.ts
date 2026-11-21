import { HttpErrorResponse } from '@angular/common/http';
import { describe, expect, it } from 'vitest';

import { studentApiErrorMessage, studentEnvelopeError } from './student-api-errors';

describe('student API error messages', () => {
  it('maps common HTTP failures to student-facing Vietnamese copy', () => {
    expect(studentApiErrorMessage(new HttpErrorResponse({ status: 401 }))).toContain(
      'Phiên đăng nhập',
    );
    expect(studentApiErrorMessage(new HttpErrorResponse({ status: 403 }))).toContain(
      'không có quyền',
    );
    expect(studentApiErrorMessage(new HttpErrorResponse({ status: 404 }))).toContain(
      'Không tìm thấy',
    );
    expect(studentApiErrorMessage(new HttpErrorResponse({ status: 0 }))).toContain(
      'Không thể kết nối',
    );
  });

  it('does not expose transport or backend messages to the page', () => {
    expect(studentApiErrorMessage(new Error('HTTP 500: SQL error'))).toBe(
      'Đã xảy ra lỗi. Vui lòng thử lại.',
    );
    expect(studentEnvelopeError(false, 'Internal server error')).toBe(
      'Yêu cầu chưa được hoàn tất. Vui lòng thử lại.',
    );
    expect(studentEnvelopeError(true, '')).toBeNull();
  });
});
