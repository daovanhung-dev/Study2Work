import { Controller, Get } from "@nestjs/common";

import { ApiSuccess } from "../common/decorators/api-success.decorator.js";
import { Public } from "../common/decorators/public.decorator.js";

@Public()
@Controller()
export class SystemController {
  @Get()
  @ApiSuccess("SYSTEM_ROOT_LOADED", "Welcome to Study2Work.")
  root() {
    return { service: "work-api" };
  }
}
