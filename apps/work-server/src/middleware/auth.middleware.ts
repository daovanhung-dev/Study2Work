import { NextFunction, Request, Response } from "express";
import { randomUUID } from "node:crypto";
import { TokenPayload, verifyToken } from "../utils/jwt.js";

function rejectAuthentication(req: Request, res: Response, status: 401 | 403): void {
  const trace = req.get("X-Trace-Id") || randomUUID();
  res.setHeader("X-Trace-Id", trace);
  res.status(status).json({
    success: false,
    businessCode: status === 401 ? "UNAUTHORIZED" : "FORBIDDEN",
    message: status === 401 ? "Yêu cầu Bearer token hợp lệ." : "Bạn không có quyền truy cập.",
    data: null,
    meta: {},
    traceId: trace,
  });
}

function extractBearerToken(req: Request): string | null {
  const authorization = req.get("authorization");
  if (!authorization) return null;

  const match = authorization.match(/^Bearer\s+([^\s]+)$/i);
  return match?.[1] ?? null;
}

/** Parse the optional Bearer token once for every request. */
export function authenticateToken(req: Request, _res: Response, next: NextFunction): void {
  const token = extractBearerToken(req);
  if (!token) {
    next();
    return;
  }

  try {
    req.user = verifyToken(token);
  } catch {
    req.authenticated = false;
  }

  next();
}

export function ensureAuthenticated(req: Request, res: Response, next: NextFunction): void {
  if (req.user && req.authenticated !== false) {
    next();
    return;
  }

  rejectAuthentication(req, res, 401);
}

export function checkRole(role: string) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const user = req.user as TokenPayload | undefined;
    if (user && req.authenticated !== false && user.role === role) {
      next();
      return;
    }

    rejectAuthentication(req, res, req.user ? 403 : 401);
  };
}
