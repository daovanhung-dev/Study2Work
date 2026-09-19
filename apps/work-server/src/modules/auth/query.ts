import type { PrismaClient } from "@prisma/client";

export function findStudentCredentials(prisma: PrismaClient, email: string) {
  return prisma.sinhVien.findUnique({
    where: { email },
    select: { id: true, email: true, matkhau: true },
  });
}

export function findBusinessCredentials(prisma: PrismaClient, email: string) {
  return prisma.doanhNghiep.findUnique({
    where: { email },
    select: { id: true, email: true, matkhau: true },
  });
}

export function rehashStudentPassword(prisma: PrismaClient, id: bigint, password: string) {
  return prisma.sinhVien.update({ where: { id }, data: { matkhau: password } });
}

export function rehashBusinessPassword(prisma: PrismaClient, id: bigint, password: string) {
  return prisma.doanhNghiep.update({ where: { id }, data: { matkhau: password } });
}
