import { randomUUID } from "node:crypto";

export const TRACE_HEADER = "X-Trace-Id";
const UUID_PATTERN =
  /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;

export function normalizeTraceId(value: string | undefined): string {
  if (value && UUID_PATTERN.test(value)) {
    return value.toLowerCase();
  }

  return randomUUID();
}
