import { z } from "zod";

const optionalText = z.string().trim().optional();

export const jobsQuerySchema = z.object({
  page: z.string().regex(/^\d+$/, "Page hoặc limit không hợp lệ.").transform(Number).refine((value) => value > 0, "Page hoặc limit không hợp lệ.").optional(),
  limit: z.string().regex(/^\d+$/, "Page hoặc limit không hợp lệ.").transform(Number).refine((value) => value > 0 && value <= 50, "Page hoặc limit không hợp lệ.").optional(),
});

export const jobIdSchema = z.string()
  .regex(/^\d+$/, "ID việc làm không hợp lệ.")
  .transform(Number)
  .refine((value) => Number.isSafeInteger(value) && value > 0, "ID việc làm không hợp lệ.");

export const jobMutationSchema = z.object({
  ten_vi_tri: optionalText,
  phong_ban: optionalText,
  cap_bac: optionalText,
  bao_cao_cho: optionalText,
  nhiem_vu: optionalText,
  trinh_do: optionalText,
  kinh_nghiem: optionalText,
  ky_nang: optionalText,
  ky_nang_mem: optionalText,
  uu_tien: optionalText,
  muc_luong: optionalText,
  phuc_loi: optionalText,
  moi_truong: optionalText,
  dia_diem: optionalText,
  thoi_gian: optionalText,
  han_nop: optionalText,
  cach_ung_tuyen: optionalText,
  mo_ta: optionalText,
  ten_cong_ty: optionalText,
  nganh: optionalText,
}).passthrough();

export type JobMutation = z.infer<typeof jobMutationSchema>;
