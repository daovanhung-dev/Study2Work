import { HttpErrorResponse } from '@angular/common/http';

export type AuthorizationErrorState =
  | {
      kind: 'authentication-required';
      status: 401;
      message: string;
      traceId: string | null;
      traceIdConflict: boolean;
    }
  | {
      kind: 'access-denied';
      status: 403;
      message: string;
      traceId: string | null;
      traceIdConflict: boolean;
    };

interface ErrorEnvelope {
  success: false;
  businessCode: string;
  message: string;
  traceId?: unknown;
}

export function normalizeAuthorizationError(error: unknown): AuthorizationErrorState | null {
  if (!(error instanceof HttpErrorResponse)) return null;
  if (error.status !== 401 && error.status !== 403) return null;

  const envelope = asErrorEnvelope(error.error);
  const expectedBusinessCode =
    error.status === 401 ? 'DESIGN_AUTHENTICATION_REQUIRED' : 'DESIGN_ACCESS_DENIED';
  if (!envelope || envelope.businessCode !== expectedBusinessCode) return null;

  const message = envelope.message.trim();
  if (!message) return null;

  const bodyTraceId = nonEmptyString(envelope.traceId);
  const headerTraceId = nonEmptyString(error.headers.get('X-Trace-Id'));
  const traceIdConflict =
    bodyTraceId !== null && headerTraceId !== null && bodyTraceId !== headerTraceId;
  const traceId = traceIdConflict ? null : (bodyTraceId ?? headerTraceId);

  if (error.status === 401) {
    return {
      kind: 'authentication-required',
      status: 401,
      message,
      traceId,
      traceIdConflict,
    };
  }

  return {
    kind: 'access-denied',
    status: 403,
    message,
    traceId,
    traceIdConflict,
  };
}

function asErrorEnvelope(value: unknown): ErrorEnvelope | null {
  if (!isRecord(value)) return null;
  if (value['success'] !== false) return null;
  if (typeof value['businessCode'] !== 'string') return null;
  if (typeof value['message'] !== 'string') return null;

  return {
    success: false,
    businessCode: value['businessCode'],
    message: value['message'],
    traceId: value['traceId'],
  };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function nonEmptyString(value: unknown): string | null {
  return typeof value === 'string' && value.trim().length > 0 ? value : null;
}
