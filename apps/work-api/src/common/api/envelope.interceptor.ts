import {
  CallHandler,
  ExecutionContext,
  Injectable,
  NestInterceptor,
} from "@nestjs/common";
import type { FastifyRequest } from "fastify";
import { Observable, map } from "rxjs";

import {
  ApiHandlerResult,
  ApiSuccessEnvelope,
  createSuccessEnvelope,
} from "./envelope";

@Injectable()
export class EnvelopeInterceptor implements NestInterceptor {
  intercept(
    context: ExecutionContext,
    next: CallHandler<ApiHandlerResult>,
  ): Observable<ApiSuccessEnvelope> {
    const request = context.switchToHttp().getRequest<FastifyRequest & { traceId?: string }>();
    const traceId = request.traceId ?? "";

    return next.handle().pipe(map((result) => createSuccessEnvelope(result, traceId)));
  }
}
