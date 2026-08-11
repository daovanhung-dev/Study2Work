import { Module, type DynamicModule } from "@nestjs/common";

import { AuthModule } from "./auth/auth.module.js";
import { WorkConfigModule } from "./config/config.module.js";
import type { WorkEnvironment } from "./config/env.js";
import { DatabaseModule } from "./database/database.module.js";
import { HttpModule } from "./common/http/http.module.js";
import { HealthModule } from "./health/health.module.js";
import { SystemModule } from "./system/system.module.js";

@Module({})
export class AppModule {
  static forRoot(environment?: WorkEnvironment): DynamicModule {
    return {
      module: AppModule,
      imports: [
        WorkConfigModule.forRoot(environment),
        DatabaseModule,
        HttpModule,
        AuthModule,
        HealthModule,
        SystemModule,
      ],
    };
  }
}
