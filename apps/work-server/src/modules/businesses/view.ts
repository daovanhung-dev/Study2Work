import type { PrismaExecutor } from "../../core/database.js";
import { ApiError } from "../../core/responses.js";
import type { UseCaseResult } from "../../core/use-case.js";
import { findBusiness } from "./query.js";

export async function getBusinessMe(prisma: PrismaExecutor, id: number): Promise<UseCaseResult> {
  const data = await findBusiness(prisma, id);
  if (!data) throw new ApiError({ statusCode: 404, businessCode: "USER_NOT_FOUND", message: "Không tìm thấy tài khoản." });
  return { statusCode: 200, businessCode: "ME_LOADED", message: "Đã tải thông tin tài khoản.", data: { ...data, role: "business" } };
}

export async function requireBusiness(prisma: PrismaExecutor, id: number) {
  const data = await findBusiness(prisma, id);
  if (!data) throw new ApiError({ statusCode: 404, businessCode: "USER_NOT_FOUND", message: "Không tìm thấy tài khoản doanh nghiệp." });
  return data;
}
