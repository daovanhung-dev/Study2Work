import type { Prisma } from "@prisma/client";

import type { PrismaExecutor } from "../../core/database.js";

import { businessPublicSelect, jobPublicSelect } from "../../services/public-selectors.js";

export function listJobs(prisma: PrismaExecutor) {
  return prisma.jD.findMany({ orderBy: { ngay_tao: "desc" }, select: jobPublicSelect });
}

export function findJob(prisma: PrismaExecutor, id: number) {
  return prisma.jD.findUnique({ where: { id: BigInt(id) }, select: jobPublicSelect });
}

export function findBusinessJobs(prisma: PrismaExecutor, businessId: number) {
  return prisma.jD.findMany({
    where: { doanhnghiep_id: BigInt(businessId) },
    orderBy: { id: "desc" },
    select: jobPublicSelect,
  });
}

export function insertJob(prisma: PrismaExecutor, data: Prisma.JDCreateInput) {
  return prisma.jD.create({ data, select: jobPublicSelect });
}

export function findOwnedJob(prisma: PrismaExecutor, jobId: number, businessId: number) {
  return prisma.jD.findFirst({ where: { id: BigInt(jobId), doanhnghiep_id: BigInt(businessId) }, select: { id: true } });
}

export function updateJob(prisma: PrismaExecutor, jobId: number, data: Prisma.JDUpdateInput) {
  return prisma.jD.update({ where: { id: BigInt(jobId) }, data, select: jobPublicSelect });
}

export function deleteJob(prisma: PrismaExecutor, jobId: number) {
  return prisma.jD.delete({ where: { id: BigInt(jobId) } });
}

export { businessPublicSelect };
