import type { NextFunction, Request, RequestHandler, Response } from "express";

import type { WorkConfig } from "../core/config.js";
import { ApiError } from "../core/responses.js";
import { decodeAccessToken, type WorkTokenPayload } from "../core/security/access-token.js";

function extractBearerToken(request: Request): string | null {
  const authorization = request.headers.authorization;
  if (!authorization || Array.isArray(authorization)) return null;
  const match = /^Bearer\s+([^\s]+)$/i.exec(authorization);
  return match?.[1] ?? null;
}

export function authenticateToken(config: WorkConfig): RequestHandler {
  return (request, _response, next) => {
    const token = extractBearerToken(request);
    if (!token) {
      next();
      return;
    }

    try {
      request.user = decodeAccessToken(config, token);
      request.authenticated = true;
    } catch {
      request.authenticated = false;
    }
    next();
  };
}

export function ensureAuthenticated(request: Request, _response: Response, next: NextFunction): void {
  if (request.user && request.authenticated !== false) {
    next();
    return;
  }
  next(new ApiError({
    statusCode: 401,
    businessCode: "UNAUTHORIZED",
    message: "Yêu cầu Bearer token hợp lệ.",
  }));
}

export function checkRole(role: "student" | "business") {
  return (request: Request, _response: Response, next: NextFunction): void => {
    const user = request.user as WorkTokenPayload | undefined;
    if (user && request.authenticated !== false && user.role === role) {
      next();
      return;
    }

    next(new ApiError({
      statusCode: user ? 403 : 401,
      businessCode: user ? "FORBIDDEN" : "UNAUTHORIZED",
      message: user ? "Bạn không có quyền truy cập." : "Yêu cầu Bearer token hợp lệ.",
    }));
  };
}

export type AuthenticatedRequest = Request & {
  user: WorkTokenPayload;
};
