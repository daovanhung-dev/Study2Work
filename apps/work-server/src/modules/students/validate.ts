import { ApiError } from "../../core/responses.js";

export function validateStudentRegistration(input: { hoten: string; email: string; matkhau: string }): void {
  if (!input.hoten || !input.email || !input.matkhau) {
    throw new ApiError({ statusCode: 400, businessCode: "INVALID_REQUEST", message: "Họ tên, email và mật khẩu bắt buộc." });
  }
}
