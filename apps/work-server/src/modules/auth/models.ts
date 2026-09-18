import { z } from "zod";

export const loginRequestSchema = z.object({
  email: z.string({ required_error: "Email và mật khẩu bắt buộc." }).trim().email("Email không hợp lệ."),
  password: z.string().min(1, "Email và mật khẩu bắt buộc.").optional(),
  matkhau: z.string().min(1, "Email và mật khẩu bắt buộc.").optional(),
}).superRefine((value, context) => {
  if (!value.password && !value.matkhau) {
    context.addIssue({ code: z.ZodIssueCode.custom, path: ["password"], message: "Email và mật khẩu bắt buộc." });
  }
});

export type LoginRequest = z.infer<typeof loginRequestSchema>;

export function loginPassword(request: LoginRequest): string {
  return request.password ?? request.matkhau ?? "";
}
