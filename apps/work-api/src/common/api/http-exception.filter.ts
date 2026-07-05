import {
  ArgumentsHost,
  Catch,
  ExceptionFilter,
  HttpException,
  HttpStatus,
} from "@nestjs/common";
import type { FastifyReply, FastifyRequest } from "fastify";

import { ApiErrorDetail, createErrorEnvelope } from "./envelope";

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function extractErrors(value: unknown): ApiErrorDetail[] {
  if (!isRecord(value) || !Array.isArray(value.errors)) {
    return [];
  }

  return value.errors
    .filter(isRecord)
    .map((item) => ({
      field: typeof item.field === "string" ? item.field : undefined,
      code: typeof item.code === "string" ? item.code : "HTTP_ERROR",
      message: typeof item.message === "string" ? item.message : "Request failed.",
    }));
}

@Catch()
export class ApiExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost): void {
    const context = host.switchToHttp();
    const reply = context.getResponse<FastifyReply>();
    const request = context.getRequest<FastifyRequest & { traceId?: string }>();
    const traceId = request.traceId ?? "";

    if (exception instanceof HttpException) {
      const status = exception.getStatus();
      const response = exception.getResponse();
      const responseRecord = isRecord(response) ? response : {};
      const message =
        typeof responseRecord.message === "string"
          ? responseRecord.message
          : exception.message;
      const businessCode =
        typeof responseRecord.businessCode === "string"
          ? responseRecord.businessCode
          : "SYSTEM_HTTP_ERROR";

      reply.status(status).send(
        createErrorEnvelope({
          businessCode,
          message,
          errors: extractErrors(responseRecord),
          traceId,
        }),
      );
      return;
    }

    reply.status(HttpStatus.INTERNAL_SERVER_ERROR).send(
      createErrorEnvelope({
        businessCode: "SYSTEM_INTERNAL_ERROR",
        message: "Internal server error.",
        errors: [
          {
            code: "INTERNAL_SERVER_ERROR",
            message: "Internal server error.",
          },
        ],
        traceId,
      }),
    );
  }
}
