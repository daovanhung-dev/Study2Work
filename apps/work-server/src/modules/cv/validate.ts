import { ApiError } from "../../core/responses.js";

const fields = [
  "hoten", "ngaysinh", "gioitinh", "email", "sdt", "diachi", "vitri", "nganh",
  "muctieunghiep", "hocvan", "kinhnghiem", "kynang", "ngoaingu", "chungchi",
  "duan", "giaithuong", "hoatdong", "portfolio", "luongmongmuon",
];

export function normalizeCvData(input: Record<string, unknown>, fileName?: string): Record<string, unknown> {
  const data: Record<string, unknown> = {};
  for (const field of fields) {
    if (input[field] !== undefined) data[field] = input[field];
  }
  if (input.ngaysinh) {
    const date = new Date(String(input.ngaysinh));
    if (Number.isNaN(date.getTime())) {
      throw new ApiError({ statusCode: 400, businessCode: "INVALID_REQUEST", message: "Ngày sinh không hợp lệ." });
    }
    data.ngaysinh = date;
  } else if ("ngaysinh" in input) {
    data.ngaysinh = null;
  }
  if (input.social !== undefined) {
    if (typeof input.social === "string" && input.social.trim()) {
      try {
        data.social = JSON.parse(input.social);
      } catch {
        data.social = input.social;
      }
    }
  }
  if (fileName) data.avt = fileName;
  return data;
}

export function validateCvData(data: Record<string, unknown>, partial: boolean): void {
  if (!partial || data.hoten !== undefined) {
    if (typeof data.hoten !== "string" || !data.hoten.trim()) {
      throw new ApiError({ statusCode: 400, businessCode: "INVALID_REQUEST", message: "Họ tên CV bắt buộc." });
    }
    data.hoten = data.hoten.trim();
  }
  if (!partial || data.email !== undefined) {
    if (typeof data.email !== "string" || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email.trim())) {
      throw new ApiError({ statusCode: 400, businessCode: "INVALID_REQUEST", message: "Email CV không hợp lệ." });
    }
    data.email = data.email.trim();
  }
  if (partial && Object.keys(data).length === 0) {
    throw new ApiError({ statusCode: 400, businessCode: "INVALID_REQUEST", message: "Cần ít nhất một trường để cập nhật CV." });
  }
}
