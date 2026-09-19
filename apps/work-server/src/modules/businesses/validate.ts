import { ApiError } from "../../core/responses.js";

export function assertBusinessOwner(userRole: string): void {
  if (userRole !== "business") {
    throw new ApiError({ statusCode: 403, businessCode: "FORBIDDEN", message: "Bạn không có quyền truy cập." });
  }
}
