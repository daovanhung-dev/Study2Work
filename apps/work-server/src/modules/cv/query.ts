import type { Prisma } from "@prisma/client";

import type { PrismaExecutor } from "../../core/database.js";

export function countStudentCvs(prisma: PrismaExecutor, studentId: number) {
  return prisma.cv.count({ where: { sinhvien_id: BigInt(studentId) } });
}

export function findStudentCv(prisma: PrismaExecutor, studentId: number) {
  return prisma.cv.findFirst({ where: { sinhvien_id: BigInt(studentId) } });
}

export function findOwnedCv(prisma: PrismaExecutor, cvId: number, studentId: number) {
  return prisma.cv.findFirst({ where: { id: BigInt(cvId), sinhvien_id: BigInt(studentId) }, select: { id: true } });
}

export function insertCv(prisma: PrismaExecutor, data: Prisma.CvCreateInput) {
  return prisma.cv.create({ data });
}

export function updateCv(prisma: PrismaExecutor, cvId: number, data: Prisma.CvUpdateInput) {
  return prisma.cv.update({ where: { id: BigInt(cvId) }, data });
}
