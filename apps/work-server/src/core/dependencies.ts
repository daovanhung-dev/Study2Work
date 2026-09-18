import type { PrismaClient } from "@prisma/client";

import { createPrismaClient } from "./database.js";
import type { WorkConfig } from "./config.js";

export interface WorkDependencies {
  config: WorkConfig;
  prisma: PrismaClient;
}

export function createDependencies(config: WorkConfig): WorkDependencies {
  return { config, prisma: createPrismaClient(config) };
}
