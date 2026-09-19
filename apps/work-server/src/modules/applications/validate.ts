import { ApiError } from "../../core/responses.js";
import { applicationJobIdSchema } from "./models.js";

export function parseApplicationId(value: string | string[], message = "ID việc làm không hợp lệ."): number {
  const parsed = typeof value === "string" ? applicationJobIdSchema.safeParse(value) : null;
  if (!parsed?.success) {
    throw new ApiError({ statusCode: 400, businessCode: "INVALID_REQUEST", message });
  }
  return parsed.data;
}
