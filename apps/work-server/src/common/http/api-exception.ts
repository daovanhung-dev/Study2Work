import { HttpException, type HttpExceptionOptions } from "@nestjs/common";

import type { ApiErrorDetail } from "./api-envelope.js";

/** A controlled error whose body is always rendered by ApiExceptionFilter. */
export class ApiException extends HttpException {
  readonly businessCode: string;
  readonly safeMessage: string;
  readonly fieldErrors: ApiErrorDetail[];

  constructor(
    statusCode: number,
    businessCode: string,
    safeMessage: string,
    fieldErrors: ApiErrorDetail[] = [],
    options?: HttpExceptionOptions,
  ) {
    super(
      {
        businessCode,
        message: safeMessage,
        data: null,
        meta: { fieldErrors },
      },
      statusCode,
      options,
    );
    this.businessCode = businessCode;
    this.safeMessage = safeMessage;
    this.fieldErrors = fieldErrors;
  }
}
