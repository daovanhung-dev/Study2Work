import { HttpStatus, Inject, Injectable } from "@nestjs/common";

import { ApiException } from "../common/http/api-exception.js";
import { WORK_ENV, type WorkEnvironment } from "../config/env.js";
import { PrismaService } from "../database/prisma.service.js";

@Injectable()
export class HealthService {
  constructor(
    @Inject(WORK_ENV) private readonly environment: WorkEnvironment,
    @Inject(PrismaService) private readonly prisma: PrismaService,
  ) {}

  live(): { service: string; environment: WorkEnvironment["appEnv"] } {
    return {
      service: "work-api",
      environment: this.environment.appEnv,
    };
  }

  async ready(): Promise<{
    service: string;
    environment: WorkEnvironment["appEnv"];
    dependencies: { database: "configured"; redis: "configured" | "not_configured" };
  }> {
    try {
      await this.prisma.$queryRaw`SELECT 1`;
    } catch {
      throw new ApiException(
        HttpStatus.SERVICE_UNAVAILABLE,
        "DEPENDENCY_UNAVAILABLE",
        "Work API is not ready.",
      );
    }

    return {
      service: "work-api",
      environment: this.environment.appEnv,
      dependencies: {
        database: "configured",
        redis: this.environment.redisUrl ? "configured" : "not_configured",
      },
    };
  }
}
