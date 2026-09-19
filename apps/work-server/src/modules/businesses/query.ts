import type { PrismaExecutor } from "../../core/database.js";

import { businessPublicSelect } from "../../services/public-selectors.js";

export function findBusiness(prisma: PrismaExecutor, id: number) {
  return prisma.doanhNghiep.findUnique({ where: { id: BigInt(id) }, select: businessPublicSelect });
}
