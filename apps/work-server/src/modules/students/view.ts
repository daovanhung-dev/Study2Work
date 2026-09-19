import type { PrismaClient } from "@prisma/client";

import { ApiError } from "../../core/responses.js";
import { hashPassword } from "../../core/security/password.js";
import type { UseCaseResult } from "../../core/use-case.js";
import { isUniqueConstraintError } from "../../utils/prisma-errors.js";
import { insertStudent, findStudent } from "./query.js";
import { validateStudentRegistration } from "./validate.js";

export async function registerStudent(
  prisma: PrismaClient,
  input: { hoten: string; email: string; matkhau: string; chuyennganh?: string; avt?: string | null },
): Promise<UseCaseResult> {
  validateStudentRegistration(input);
  try {
    const data = await insertStudent(prisma, { ...input, matkhau: await hashPassword(input.matkhau) });
    return {
      statusCode: 201,
      businessCode: "STUDENT_CREATED",
      message: "Bạn đã tạo tài khoản thành công.",
      data,
    };
  } catch (error) {
    if (isUniqueConstraintError(error)) {
      throw new ApiError({ statusCode: 409, businessCode: "STUDENT_CREATE_FAILED", message: "Email đã được đăng ký." });
    }
    throw error;
  }
}

export async function getStudentMe(prisma: PrismaClient, id: number): Promise<UseCaseResult> {
  const data = await findStudent(prisma, id);
  if (!data) throw new ApiError({ statusCode: 404, businessCode: "USER_NOT_FOUND", message: "Không tìm thấy tài khoản." });
  return { statusCode: 200, businessCode: "ME_LOADED", message: "Đã tải thông tin tài khoản.", data: { ...data, role: "student" } };
}
