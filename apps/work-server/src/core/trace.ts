import { AsyncLocalStorage } from "node:async_hooks";
import { randomUUID } from "node:crypto";

import type { Request } from "express";

export const TRACE_HEADER = "X-Trace-Id";

const traceStorage = new AsyncLocalStorage<string>();

export function createTraceId(): string {
  return randomUUID();
}

export function validateTraceId(value: string | undefined): string | null {
  if (!value) return null;
  const normalized = value.trim();
  const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  return uuidPattern.test(normalized) ? normalized.toLowerCase() : null;
}

export function getTraceId(request: Request): string {
  const existing = validateTraceId(request.traceId);
  if (existing) return existing;
  const generated = createTraceId();
  request.traceId = generated;
  return generated;
}

export function getCurrentTraceId(): string | undefined {
  return traceStorage.getStore();
}

export function runWithTraceId<T>(traceId: string, callback: () => T): T {
  return traceStorage.run(traceId, callback);
}
