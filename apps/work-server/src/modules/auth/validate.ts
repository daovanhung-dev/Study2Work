import { ApiError } from "../../core/responses.js";

export function assertLoginPassword(password: string): void {
  if (!password) {
    throw new ApiError({ statusCode: 400, businessCode: "INVALID_REQUEST", message: "Email và mật khẩu bắt buộc." });
  }
}
