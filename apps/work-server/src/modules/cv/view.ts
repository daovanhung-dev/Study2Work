import type { PrismaClient } from "@prisma/client";

import { ApiError } from "../../core/responses.js";
import type { UseCaseResult } from "../../core/use-case.js";
import { isUniqueConstraintError } from "../../utils/prisma-errors.js";
import { countStudentCvs, findOwnedCv, findStudentCv, insertCv, updateCv as updateCvRecord } from "./query.js";
import { cvIdSchema } from "./models.js";
import { normalizeCvData, validateCvData } from "./validate.js";

export async function getMyCv(prisma: PrismaClient, studentId: number): Promise<UseCaseResult> {
  const data = await findStudentCv(prisma, studentId);
  if (!data) throw new ApiError({ statusCode: 404, businessCode: "CV_NOT_FOUND", message: "Chưa tìm thấy CV." });
  return { statusCode: 200, businessCode: "CV_LOADED", message: "Đã tải CV.", data };
}

export async function createCv(
  prisma: PrismaClient,
  studentId: number,
  body: Record<string, unknown>,
  fileName?: string,
): Promise<UseCaseResult> {
  const data = normalizeCvData(body, fileName);
  validateCvData(data, false);
  try {
    const created = await prisma.$transaction(async (transaction) => {
      if (await countStudentCvs(transaction, studentId) > 0) {
        throw new ApiError({ statusCode: 409, businessCode: "CV_ALREADY_EXISTS", message: "Tài khoản đã có CV." });
      }
      return insertCv(transaction, { ...data, sinhvien_id: BigInt(studentId) } as never);
    });
    return { statusCode: 201, businessCode: "CV_CREATED", message: "Tạo CV thành công.", data: created };
  } catch (error) {
    if (isUniqueConstraintError(error)) {
      throw new ApiError({ statusCode: 409, businessCode: "CV_ALREADY_EXISTS", message: "Tài khoản đã có CV." });
    }
    throw error;
  }
}

export async function updateCv(
  prisma: PrismaClient,
  studentId: number,
  rawCvId: string | string[],
  body: Record<string, unknown>,
  fileName?: string,
): Promise<UseCaseResult> {
  const cvId = parseCvId(rawCvId);
  const data = normalizeCvData(body, fileName);
  validateCvData(data, true);
  const updated = await prisma.$transaction(async (transaction) => {
    if (!await findOwnedCv(transaction, cvId, studentId)) {
      throw new ApiError({ statusCode: 404, businessCode: "CV_NOT_FOUND", message: "Không tìm thấy CV của tài khoản." });
    }
    return updateCvRecord(transaction, cvId, data as never);
  });
  return { statusCode: 200, businessCode: "CV_UPDATED", message: "Cập nhật CV thành công.", data: updated };
}

export async function getStudentCv(prisma: PrismaClient, rawStudentId: string | string[]): Promise<UseCaseResult> {
  const studentId = parseCvId(rawStudentId, "ID sinh viên không hợp lệ.");
  const data = await findStudentCv(prisma, studentId);
  if (!data) throw new ApiError({ statusCode: 404, businessCode: "CV_NOT_FOUND", message: "Không tìm thấy CV." });
  return { statusCode: 200, businessCode: "CV_LOADED", message: "Đã tải CV ứng viên.", data };
}

function parseCvId(value: string | string[], message = "ID CV không hợp lệ."): number {
  const parsed = typeof value === "string" ? cvIdSchema.safeParse(value) : null;
  if (!parsed?.success) {
    throw new ApiError({ statusCode: 400, businessCode: "INVALID_REQUEST", message });
  }
  return parsed.data;
}
