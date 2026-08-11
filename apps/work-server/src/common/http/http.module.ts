import { Module } from "@nestjs/common";
import { APP_FILTER, APP_INTERCEPTOR } from "@nestjs/core";

import { ApiEnvelopeInterceptor } from "./api-envelope.interceptor.js";
import { ApiExceptionFilter } from "./api-exception.filter.js";

@Module({
  providers: [
    ApiEnvelopeInterceptor,
    ApiExceptionFilter,
    {
      provide: APP_INTERCEPTOR,
      useExisting: ApiEnvelopeInterceptor,
    },
    {
      provide: APP_FILTER,
      useExisting: ApiExceptionFilter,
    },
  ],
})
export class HttpModule {}
