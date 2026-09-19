import { PrismaClient, type Prisma } from "@prisma/client";

import type { WorkConfig } from "./config.js";

export function createPrismaClient(config: WorkConfig): PrismaClient {
  return new PrismaClient({
    datasources: {
      db: { url: config.databaseUrl },
    },
  });
}

export type PrismaExecutor = PrismaClient | Prisma.TransactionClient;

export async function probeDatabase(prisma: PrismaClient): Promise<void> {
  await prisma.$queryRaw`SELECT 1`;
}
