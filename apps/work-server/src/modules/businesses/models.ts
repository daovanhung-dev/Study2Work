import { z } from "zod";

export const businessJobOwnerSchema = z.object({
  ten_vi_tri: z.string().trim().min(1, "Tên vị trí và địa điểm bắt buộc."),
  dia_diem: z.string().trim().min(1, "Tên vị trí và địa điểm bắt buộc."),
});
