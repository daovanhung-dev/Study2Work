import { Inject, Injectable, type OnModuleDestroy } from "@nestjs/common";
import { PrismaClient } from "@prisma/client";

import { WORK_ENV, type WorkEnvironment } from "../config/env.js";

/** Shared Prisma client. Domain modules inject this service rather than create clients. */
@Injectable()
export class PrismaService extends PrismaClient implements OnModuleDestroy {
  constructor(@Inject(WORK_ENV) environment: WorkEnvironment) {
    super({
      datasources: {
        db: {
          url: environment.databaseUrl,
        },
      },
      log: environment.appEnv === "production" ? ["error"] : ["error", "warn"],
    });
  }

  async onModuleDestroy(): Promise<void> {
    await this.$disconnect();
  }
}
