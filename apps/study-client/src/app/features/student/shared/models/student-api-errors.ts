export function studentApiErrorMessage(error: unknown): string {
  if (error && typeof error === 'object') {
    const candidate = error as { error?: { message?: unknown }; message?: unknown };
    if (typeof candidate.error?.message === 'string' && candidate.error.message.trim())
      return candidate.error.message;
    if (typeof candidate.message === 'string' && candidate.message.trim()) return candidate.message;
  }
  return 'Không thể tải dữ liệu từ Study Server. Vui lòng thử lại.';
}

export function studentEnvelopeError(success: boolean, message: string): string | null {
  return success ? null : message || 'Study Server không trả dữ liệu thành công.';
}
