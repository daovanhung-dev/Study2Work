import type { PrismaClient } from "@prisma/client";

import { studentPublicSelect } from "../../services/public-selectors.js";

export function insertStudent(
  prisma: PrismaClient,
  input: { hoten: string; email: string; matkhau: string; chuyennganh?: string; avt?: string | null },
) {
  return prisma.sinhVien.create({
    data: {
      hoten: input.hoten,
      email: input.email,
      matkhau: input.matkhau,
      chuyennganh: input.chuyennganh ?? "",
      avt: input.avt ?? null,
    },
    select: studentPublicSelect,
  });
}

export function findStudent(prisma: PrismaClient, id: number) {
  return prisma.sinhVien.findUnique({ where: { id: BigInt(id) }, select: studentPublicSelect });
}
