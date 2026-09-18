import type { PrismaExecutor } from "../../core/database.js";

import { businessPublicSelect, jobPublicSelect, studentPublicSelect } from "../../services/public-selectors.js";

export function findJobForApplication(prisma: PrismaExecutor, jobId: number) {
  return prisma.jD.findUnique({ where: { id: BigInt(jobId) }, select: { doanhnghiep_id: true } });
}

export function countApplications(prisma: PrismaExecutor, studentId: number, businessId: number, jobId: number) {
  return prisma.ungVien.count({
    where: { sinhvien_id: BigInt(studentId), doanhnghiep_id: BigInt(businessId), jd_id: BigInt(jobId) },
  });
}

export function insertApplication(prisma: PrismaExecutor, studentId: number, businessId: number, jobId: number) {
  return prisma.ungVien.create({
    data: { sinhvien_id: BigInt(studentId), doanhnghiep_id: BigInt(businessId), jd_id: BigInt(jobId) },
    include: { JD: { select: jobPublicSelect } },
  });
}

export function listStudentApplications(prisma: PrismaExecutor, studentId: number) {
  return prisma.ungVien.findMany({
    where: { sinhvien_id: BigInt(studentId) },
    include: { JD: { select: jobPublicSelect }, DoanhNghiep: { select: businessPublicSelect } },
    orderBy: { created_at: "desc" },
  });
}

export function listBusinessApplications(prisma: PrismaExecutor, businessId: number) {
  return prisma.ungVien.findMany({
    where: { doanhnghiep_id: BigInt(businessId) },
    include: { SinhVien: { select: studentPublicSelect }, JD: { select: jobPublicSelect } },
  });
}
