import type { PrismaClient } from "@prisma/client";

import { ApiError } from "../../core/responses.js";
import type { UseCaseResult } from "../../core/use-case.js";
import { isUniqueConstraintError } from "../../utils/prisma-errors.js";
import { countApplications, findJobForApplication, insertApplication, listBusinessApplications, listStudentApplications } from "./query.js";
import { parseApplicationId } from "./validate.js";

export async function applyToJob(prisma: PrismaClient, studentId: number, rawJobId: string | string[]): Promise<UseCaseResult> {
  const jobId = parseApplicationId(rawJobId);
  try {
    const application = await prisma.$transaction(async (transaction) => {
      const job = await findJobForApplication(transaction, jobId);
      if (!job) throw new ApiError({ statusCode: 404, businessCode: "JOB_NOT_FOUND", message: "Vị trí ứng tuyển không tồn tại." });
      if (!job.doanhnghiep_id) throw new ApiError({ statusCode: 400, businessCode: "INVALID_REQUEST", message: "Vị trí chưa gán doanh nghiệp." });

      const businessId = Number(job.doanhnghiep_id);
      if (!Number.isSafeInteger(businessId) || businessId < 1) {
        throw new ApiError({ statusCode: 500, businessCode: "INTERNAL_SERVER_ERROR", message: "Lỗi máy chủ." });
      }
      if (await countApplications(transaction, studentId, businessId, jobId) > 0) {
        throw new ApiError({ statusCode: 409, businessCode: "APPLICATION_ALREADY_EXISTS", message: "Bạn đã ứng tuyển vị trí này rồi." });
      }
      return insertApplication(transaction, studentId, businessId, jobId);
    });
    return {
      statusCode: 201,
      businessCode: "APPLICATION_CREATED",
      message: "Ứng tuyển thành công.",
      data: application,
    };
  } catch (error) {
    if (isUniqueConstraintError(error)) {
      throw new ApiError({ statusCode: 409, businessCode: "APPLICATION_ALREADY_EXISTS", message: "Bạn đã ứng tuyển vị trí này rồi." });
    }
    throw error;
  }
}

export async function getStudentApplications(prisma: PrismaClient, studentId: number): Promise<UseCaseResult> {
  return { statusCode: 200, businessCode: "APPLICATIONS_LOADED", message: "Đã tải kết quả ứng tuyển.", data: await listStudentApplications(prisma, studentId) };
}

export async function getBusinessApplications(prisma: PrismaClient, businessId: number): Promise<UseCaseResult> {
  return { statusCode: 200, businessCode: "BUSINESS_APPLICATIONS_LOADED", message: "Đã tải danh sách ứng viên.", data: await listBusinessApplications(prisma, businessId) };
}
