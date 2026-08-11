import { randomUUID } from "node:crypto";

export const TRACE_ID_HEADER = "X-Trace-Id";

const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export function normalizeTraceId(value: string | undefined): string | undefined {
  const candidate = value?.trim();
  return candidate && UUID_PATTERN.test(candidate) ? candidate.toLowerCase() : undefined;
}

export function createTraceId(): string {
  return randomUUID();
}
