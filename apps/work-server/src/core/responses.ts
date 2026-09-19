import type { Response } from "express";

import { getTraceId, TRACE_HEADER } from "./trace.js";
import type { Request } from "express";

export interface ErrorDetail {
  field?: string;
  code: string;
  message: string;
}

export interface ApiEnvelope<T = unknown> {
  success: boolean;
  businessCode: string;
  message: string;
  data: T | null;
  meta: Record<string, unknown>;
  traceId: string;
}

export class ApiError extends Error {
  readonly statusCode: number;
  readonly businessCode: string;
  readonly errors: ErrorDetail[];
  readonly headers: Record<string, string>;

  constructor(options: {
    statusCode: number;
    businessCode: string;
    message: string;
    errors?: ErrorDetail[];
    headers?: Record<string, string>;
  }) {
    super(options.message);
    this.name = "ApiError";
    this.statusCode = options.statusCode;
    this.businessCode = options.businessCode;
    this.errors = options.errors ?? [];
    this.headers = options.headers ?? {};
  }
}

export function jsonSafe(value: unknown): unknown {
  if (typeof value === "bigint") return Number(value);
  if (value instanceof Date) return value.toISOString();
  if (Array.isArray(value)) return value.map(jsonSafe);
  if (typeof value === "object" && value !== null) {
    return Object.fromEntries(
      Object.entries(value).map(([key, child]) => [key, jsonSafe(child)]),
    );
  }
  return value;
}

export function successResponse<T>(options: {
  request: Request;
  response: Response;
  statusCode: number;
  businessCode: string;
  message: string;
  data?: T;
  meta?: Record<string, unknown>;
}): Response {
  const traceId = getTraceId(options.request);
  options.response.setHeader(TRACE_HEADER, traceId);
  return options.response.status(options.statusCode).json({
    success: true,
    businessCode: options.businessCode,
    message: options.message,
    data: jsonSafe(options.data ?? null),
    meta: options.meta ?? {},
    traceId,
  } satisfies ApiEnvelope);
}

export function errorResponse(options: {
  request: Request;
  response: Response;
  statusCode: number;
  businessCode: string;
  message: string;
  errors?: ErrorDetail[];
  headers?: Record<string, string>;
}): Response {
  const traceId = getTraceId(options.request);
  const meta = options.errors?.length ? { fieldErrors: options.errors } : {};
  options.response.setHeader(TRACE_HEADER, traceId);
  for (const [key, value] of Object.entries(options.headers ?? {})) {
    options.response.setHeader(key, value);
  }
  return options.response.status(options.statusCode).json({
    success: false,
    businessCode: options.businessCode,
    message: options.message,
    data: null,
    meta,
    traceId,
  } satisfies ApiEnvelope<null>);
}

export function sendSuccess<T>(
  request: Request,
  response: Response,
  statusCode: number,
  businessCode: string,
  message: string,
  data?: T,
  meta?: Record<string, unknown>,
): Response {
  return successResponse({ request, response, statusCode, businessCode, message, data, meta });
}
