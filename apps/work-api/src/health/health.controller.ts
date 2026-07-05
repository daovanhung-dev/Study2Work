import { Controller, Get } from "@nestjs/common";

import type { ApiHandlerResult } from "../common/api/envelope";
import { loadEnv } from "../common/config/env";

@Controller("health")
export class HealthController {
  @Get("live")
  live(): ApiHandlerResult {
    const env = loadEnv();
    return {
      businessCode: "SYSTEM_HEALTH_LIVE",
      message: "Work API is live.",
      data: {
        status: "ok",
        service: "work-api",
        version: "0.1.0",
        environment: env.appEnv,
      },
    };
  }

  @Get("ready")
  ready(): ApiHandlerResult {
    const env = loadEnv();
    return {
      businessCode: "SYSTEM_HEALTH_READY",
      message: "Work API is ready.",
      data: {
        status: "ok",
        service: "work-api",
        dependencies: {
          database: "configured",
          redis: "configured",
        },
        environment: env.appEnv,
      },
    };
  }
}
