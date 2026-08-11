import {
  Catch,
  HttpException,
  HttpStatus,
  Logger,
  type ArgumentsHost,
  type ExceptionFilter,
} from "@nestjs/common";
import type { FastifyReply, FastifyRequest } from "fastify";

import { createTraceId, TRACE_ID_HEADER } from "../trace/trace-id.js";
import type { ApiErrorDetail, ApiErrorEnvelope } from "./api-envelope.js";
import { ApiException } from "./api-exception.js";

interface NormalizedException {
  statusCode: number;
  businessCode: string;
  message: string;
  fieldErrors: ApiErrorDetail[];
}

@Catch()
export class ApiExceptionFilter implements ExceptionFilter {
  private readonly logger = new Logger(ApiExceptionFilter.name);

  catch(exception: unknown, host: ArgumentsHost): void {
    const http = host.switchToHttp();
    const request = http.getRequest<FastifyRequest>();
    const reply = http.getResponse<FastifyReply>();

    if (reply.sent) {
      return;
    }

    const traceId = request.traceId ?? createTraceId();
    request.traceId = traceId;
    const normalized = this.normalize(exception);

    if (normalized.statusCode >= HttpStatus.INTERNAL_SERVER_ERROR) {
      this.logger.error(`Unhandled Work API error (traceId=${traceId})`, this.stackOf(exception));
    }

    const body: ApiErrorEnvelope = {
      success: false,
      businessCode: normalized.businessCode,
      message: normalized.message,
      data: null,
      meta: { fieldErrors: normalized.fieldErrors },
      traceId,
    };

    reply.header(TRACE_ID_HEADER, traceId).code(normalized.statusCode).send(body);
  }

  private normalize(exception: unknown): NormalizedException {
    if (exception instanceof ApiException) {
      return {
        statusCode: exception.getStatus(),
        businessCode: exception.businessCode,
        message: exception.safeMessage,
        fieldErrors: exception.fieldErrors,
      };
    }

    if (exception instanceof HttpException) {
      return {
        statusCode: exception.getStatus(),
        businessCode: "HTTP_ERROR",
        message: "The request could not be processed.",
        fieldErrors: [],
      };
    }

    const statusCode = this.statusCodeOf(exception);
    return {
      statusCode,
      businessCode:
        statusCode === HttpStatus.SERVICE_UNAVAILABLE
          ? "DEPENDENCY_UNAVAILABLE"
          : "INTERNAL_SERVER_ERROR",
      message:
        statusCode === HttpStatus.SERVICE_UNAVAILABLE
          ? "A required service is temporarily unavailable."
          : "An internal server error occurred.",
      fieldErrors: [],
    };
  }

  private statusCodeOf(exception: unknown): number {
    if (
      exception &&
      typeof exception === "object" &&
      "statusCode" in exception &&
      typeof exception.statusCode === "number" &&
      exception.statusCode >= 400 &&
      exception.statusCode <= 599
    ) {
      return exception.statusCode;
    }

    return HttpStatus.INTERNAL_SERVER_ERROR;
  }

  private stackOf(exception: unknown): string | undefined {
    return exception instanceof Error ? exception.stack : undefined;
  }
}
