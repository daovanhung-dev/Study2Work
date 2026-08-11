import { Global, Module } from "@nestjs/common";
import { APP_GUARD } from "@nestjs/core";

import { JwksAuthGuard } from "./jwks-auth.guard.js";
import { JwksAuthService } from "./jwks-auth.service.js";

@Global()
@Module({
  providers: [
    JwksAuthService,
    {
      provide: APP_GUARD,
      useClass: JwksAuthGuard,
    },
  ],
  exports: [JwksAuthService],
})
export class AuthModule {}
