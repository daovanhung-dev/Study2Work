import type { NextFunction, Request, RequestHandler, Response } from "express";

import { TRACE_HEADER, createTraceId, runWithTraceId, validateTraceId } from "./trace.js";

export const traceMiddleware: RequestHandler = (request, response, next) => {
  const traceId = validateTraceId(request.get(TRACE_HEADER)) ?? createTraceId();
  request.traceId = traceId;
  response.setHeader(TRACE_HEADER, traceId);
  runWithTraceId(traceId, next);
};

export function asyncHandler(
  handler: (request: Request, response: Response, next: NextFunction) => Promise<unknown>,
): RequestHandler {
  return (request, response, next) => {
    void handler(request, response, next).catch(next);
  };
}
