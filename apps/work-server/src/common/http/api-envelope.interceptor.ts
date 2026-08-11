import {
  Inject,
  Injectable,
  type CallHandler,
  type ExecutionContext,
  type NestInterceptor,
} from "@nestjs/common";
import { Reflector } from "@nestjs/core";
import type { FastifyRequest } from "fastify";
import { map, type Observable } from "rxjs";

import {
  API_SUCCESS_KEY,
  type ApiSuccessMetadata,
} from "../decorators/api-success.decorator.js";
import { createTraceId } from "../trace/trace-id.js";
import { isApiEnvelope, type ApiEnvelope, type ApiSuccessEnvelope } from "./api-envelope.js";

const DEFAULT_SUCCESS: ApiSuccessMetadata = {
  businessCode: "REQUEST_SUCCEEDED",
  message: "Request completed.",
};

@Injectable()
export class ApiEnvelopeInterceptor implements NestInterceptor {
  constructor(@Inject(Reflector) private readonly reflector: Reflector) {}

  intercept(context: ExecutionContext, next: CallHandler): Observable<ApiEnvelope> {
    const request = context.switchToHttp().getRequest<FastifyRequest>();
    const traceId = request.traceId ?? createTraceId();
    request.traceId = traceId;

    const metadata =
      this.reflector.getAllAndOverride<ApiSuccessMetadata>(API_SUCCESS_KEY, [
        context.getHandler(),
        context.getClass(),
      ]) ?? DEFAULT_SUCCESS;

    return next.handle().pipe(
      map((data: unknown): ApiEnvelope => {
        if (isApiEnvelope(data)) {
          return data;
        }

        const response: ApiSuccessEnvelope = {
          success: true,
          businessCode: metadata.businessCode,
          message: metadata.message,
          data: data ?? null,
          meta: metadata.meta ?? {},
          traceId,
        };
        return response;
      }),
    );
  }
}
