import { z } from "zod";

export const studentRegistrationSchema = z.object({
  hoten: z.string({ required_error: "Họ tên, email và mật khẩu bắt buộc." }).trim().min(1, "Họ tên, email và mật khẩu bắt buộc."),
  email: z.string({ required_error: "Họ tên, email và mật khẩu bắt buộc." }).trim().email("Email không hợp lệ."),
  matkhau: z.string({ required_error: "Họ tên, email và mật khẩu bắt buộc." }).min(6, "Mật khẩu phải có ít nhất 6 ký tự."),
  chuyennganh: z.string().optional(),
});

export type StudentRegistration = z.infer<typeof studentRegistrationSchema>;
