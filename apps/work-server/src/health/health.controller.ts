import { Controller, Get, Inject } from "@nestjs/common";

import { ApiSuccess } from "../common/decorators/api-success.decorator.js";
import { Public } from "../common/decorators/public.decorator.js";
import { HealthService } from "./health.service.js";

@Public()
@Controller("health")
export class HealthController {
  constructor(@Inject(HealthService) private readonly healthService: HealthService) {}

  @Get("live")
  @ApiSuccess("SYSTEM_HEALTH_LIVE", "Work API is live.")
  live() {
    return this.healthService.live();
  }

  @Get("ready")
  @ApiSuccess("SYSTEM_HEALTH_READY", "Work API is ready.")
  ready() {
    return this.healthService.ready();
  }
}
