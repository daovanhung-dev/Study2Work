import type { PrismaClient } from "@prisma/client";

import { ApiError } from "../../core/responses.js";
import type { UseCaseResult } from "../../core/use-case.js";
import { requireBusiness } from "../businesses/view.js";
import { findBusinessJobs, findJob, findOwnedJob, insertJob, listJobs, updateJob, deleteJob } from "./query.js";
import { assertCreateJob, assertPartialUpdate, normalizeJobData, parseNumericId } from "./validate.js";

export async function getJobs(prisma: PrismaClient, page = 1, limit = 6): Promise<UseCaseResult> {
  const allJobs = await listJobs(prisma);
  const total = allJobs.length;
  return {
    statusCode: 200,
    businessCode: "JOBS_LOADED",
    message: "Đã tải danh sách việc làm.",
    data: allJobs.slice((page - 1) * limit, page * limit),
    meta: { page, limit, total, totalPages: Math.ceil(total / limit) },
  };
}

export async function getJob(prisma: PrismaClient, rawId: string | string[]): Promise<UseCaseResult> {
  const id = parseNumericId(rawId, "ID việc làm không hợp lệ.");
  const data = await findJob(prisma, id);
  if (!data) throw new ApiError({ statusCode: 404, businessCode: "JOB_NOT_FOUND", message: "Không tìm thấy việc làm." });
  return { statusCode: 200, businessCode: "JOB_LOADED", message: "Đã tải chi tiết việc làm.", data };
}

export async function getBusinessJobs(prisma: PrismaClient, businessId: number): Promise<UseCaseResult> {
  return { statusCode: 200, businessCode: "BUSINESS_JOBS_LOADED", message: "Đã tải tin tuyển dụng.", data: await findBusinessJobs(prisma, businessId) };
}

export async function createBusinessJob(
  prisma: PrismaClient,
  businessId: number,
  body: Record<string, unknown>,
  fileName?: string,
): Promise<UseCaseResult> {
  const data = normalizeJobData(body, fileName);
  assertCreateJob(data);
  const created = await prisma.$transaction(async (transaction) => {
    const business = await requireBusiness(transaction, businessId);
    return insertJob(transaction, {
      ...data,
      ten_vi_tri: String(data.ten_vi_tri),
      doanhnghiep_id: BigInt(businessId),
      ten_cong_ty: data.ten_cong_ty || business.hoten || undefined,
    } as never);
  });
  return { statusCode: 201, businessCode: "JOB_CREATED", message: "Tạo tin tuyển dụng thành công.", data: created };
}

export async function updateBusinessJob(
  prisma: PrismaClient,
  businessId: number,
  rawId: string | string[],
  body: Record<string, unknown>,
  fileName?: string,
): Promise<UseCaseResult> {
  const id = parseNumericId(rawId, "ID việc làm không hợp lệ.");
  const data = normalizeJobData(body, fileName);
  assertPartialUpdate(data, "Cần ít nhất một trường để cập nhật tin tuyển dụng.");
  const updated = await prisma.$transaction(async (transaction) => {
    if (!await findOwnedJob(transaction, id, businessId)) {
      throw new ApiError({ statusCode: 404, businessCode: "JOB_NOT_FOUND", message: "Không tìm thấy tin tuyển dụng của tài khoản." });
    }
    return updateJob(transaction, id, data as never);
  });
  return { statusCode: 200, businessCode: "JOB_UPDATED", message: "Cập nhật tin tuyển dụng thành công.", data: updated };
}

export async function deleteBusinessJob(prisma: PrismaClient, businessId: number, rawId: string | string[]): Promise<UseCaseResult> {
  const id = parseNumericId(rawId, "ID việc làm không hợp lệ.");
  await prisma.$transaction(async (transaction) => {
    if (!await findOwnedJob(transaction, id, businessId)) {
      throw new ApiError({ statusCode: 404, businessCode: "JOB_NOT_FOUND", message: "Không tìm thấy tin tuyển dụng của tài khoản." });
    }
    await deleteJob(transaction, id);
  });
  return { statusCode: 200, businessCode: "JOB_DELETED", message: "Đã xóa tin tuyển dụng.", data: { id } };
}
