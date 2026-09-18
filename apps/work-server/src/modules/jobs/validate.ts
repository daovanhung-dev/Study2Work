import { ApiError } from "../../core/responses.js";
import { jobIdSchema } from "./models.js";

export function parseNumericId(value: string | string[] | undefined, message = "ID không hợp lệ."): number {
  const parsed = typeof value === "string" ? jobIdSchema.safeParse(value) : null;
  if (!parsed?.success) {
    throw new ApiError({ statusCode: 400, businessCode: "INVALID_REQUEST", message });
  }
  return parsed.data;
}

export function normalizeJobData(input: Record<string, unknown>, fileName?: string): Record<string, unknown> {
  const fields = [
    "ten_vi_tri", "phong_ban", "cap_bac", "bao_cao_cho", "nhiem_vu", "trinh_do",
    "kinh_nghiem", "ky_nang", "ky_nang_mem", "uu_tien", "muc_luong", "phuc_loi",
    "moi_truong", "dia_diem", "thoi_gian", "han_nop", "cach_ung_tuyen", "mo_ta",
    "ten_cong_ty", "nganh",
  ];
  const data: Record<string, unknown> = {};
  for (const field of fields) {
    if (input[field] !== undefined) data[field] = typeof input[field] === "string" ? input[field].trim() : input[field];
  }
  if (fileName) data.avt = `/uploads/${fileName}`;
  return data;
}

export function assertCreateJob(data: Record<string, unknown>): void {
  if (typeof data.ten_vi_tri !== "string" || !data.ten_vi_tri || typeof data.dia_diem !== "string" || !data.dia_diem) {
    throw new ApiError({ statusCode: 400, businessCode: "INVALID_REQUEST", message: "Tên vị trí và địa điểm bắt buộc." });
  }
}

export function assertPartialUpdate(data: Record<string, unknown>, message: string): void {
  if (Object.keys(data).length === 0) {
    throw new ApiError({ statusCode: 400, businessCode: "INVALID_REQUEST", message });
  }
}
