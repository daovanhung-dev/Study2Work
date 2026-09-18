import { MulterError } from "multer";
import type { ErrorRequestHandler, Request, Response, NextFunction } from "express";
import { Prisma } from "@prisma/client";
import { ZodError } from "zod";

import { ApiError, errorResponse } from "./responses.js";

function validationErrors(error: ZodError): { field?: string; code: string; message: string }[] {
  return error.issues.map((issue) => ({
    field: issue.path.length ? issue.path.join(".") : undefined,
    code: issue.code.toUpperCase(),
    message: issue.message,
  }));
}

function asApiError(error: unknown): ApiError {
  if (error instanceof ApiError) return error;
  if (error instanceof ZodError) {
    return new ApiError({
      statusCode: 400,
      businessCode: "INVALID_REQUEST",
      message: "Request không hợp lệ.",
      errors: validationErrors(error),
    });
  }
  if (error instanceof MulterError) {
    return new ApiError({
      statusCode: error.code === "LIMIT_FILE_SIZE" ? 413 : 400,
      businessCode: error.code === "LIMIT_FILE_SIZE" ? "PAYLOAD_TOO_LARGE" : "INVALID_REQUEST",
      message: error.code === "LIMIT_FILE_SIZE"
        ? "File tải lên vượt quá kích thước cho phép."
        : "Request không hợp lệ.",
    });
  }
  if (error instanceof Error && error.message === "Chỉ cho phép file ảnh (jpeg, jpg, png, gif)") {
    return new ApiError({ statusCode: 400, businessCode: "INVALID_REQUEST", message: "Request không hợp lệ." });
  }
  if (error instanceof SyntaxError && "body" in error) {
    return new ApiError({ statusCode: 400, businessCode: "INVALID_REQUEST", message: "Request không hợp lệ." });
  }
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    if (error.code === "P2002") {
      return new ApiError({ statusCode: 409, businessCode: "RESOURCE_CONFLICT", message: "Dữ liệu đã tồn tại." });
    }
    if (error.code === "P2025") {
      return new ApiError({ statusCode: 404, businessCode: "RESOURCE_NOT_FOUND", message: "Không tìm thấy tài nguyên." });
    }
  }
  return new ApiError({ statusCode: 500, businessCode: "INTERNAL_SERVER_ERROR", message: "Lỗi máy chủ." });
}

export const errorHandler: ErrorRequestHandler = (
  error: unknown,
  request: Request,
  response: Response,
  next: NextFunction,
) => {
  if (response.headersSent) {
    next(error);
    return;
  }

  const apiError = asApiError(error);
  if (apiError.statusCode >= 500 && !(error instanceof ApiError)) {
    console.error("Unhandled Work API error.");
  }
  errorResponse({
    request,
    response,
    statusCode: apiError.statusCode,
    businessCode: apiError.businessCode,
    message: apiError.message,
    errors: apiError.errors,
    headers: apiError.headers,
  });
};

export function notFoundHandler(request: Request, response: Response): void {
  errorResponse({
    request,
    response,
    statusCode: 404,
    businessCode: "NOT_FOUND",
    message: "Không tìm thấy tài nguyên.",
  });
}
