import axios, {
  type AxiosError,
  type AxiosRequestConfig,
  type InternalAxiosRequestConfig,
} from "axios";

import {
  getFieldErrors,
  isSuccessEnvelope,
  parseApiEnvelope,
  type ApiEnvelope,
  type ApiFieldError,
  type ApiMeta,
  type ApiSuccessEnvelope,
} from "./envelope";
import { identityApiBaseUrl, identityLoginUrl, workApiBaseUrl } from "./runtime";
import { restoreWorkSession } from "../session/session-client";
import { clearSession, getAccessToken, useSessionStore } from "../session/store";

export { identityApiBaseUrl, identityLoginUrl, workApiBaseUrl };

export class WorkApiError extends Error {
  readonly businessCode?: string;
  readonly fieldErrors: ApiFieldError[];
  readonly retryAfterSeconds?: number;
  readonly status?: number;
  readonly traceId?: string;

  constructor({
    message,
    status,
    businessCode,
    traceId,
    fieldErrors = [],
    retryAfterSeconds,
  }: {
    message: string;
    status?: number;
    businessCode?: string;
    traceId?: string;
    fieldErrors?: ApiFieldError[];
    retryAfterSeconds?: number;
  }) {
    super(message);
    this.name = "WorkApiError";
    this.status = status;
    this.businessCode = businessCode;
    this.traceId = traceId;
    this.fieldErrors = fieldErrors;
    this.retryAfterSeconds = retryAfterSeconds;
  }
}

function newRequestId(): string | undefined {
  return typeof crypto !== "undefined" && "randomUUID" in crypto
    ? crypto.randomUUID()
    : undefined;
}

function retryAfterSeconds(value: unknown): number | undefined {
  if (typeof value === "number" && Number.isFinite(value) && value >= 0) {
    return Math.ceil(value);
  }

  if (typeof value !== "string") {
    return undefined;
  }

  const seconds = Number.parseInt(value, 10);
  if (Number.isFinite(seconds) && /^\s*\d+\s*$/.test(value)) {
    return seconds;
  }

  const retryAt = Date.parse(value);
  return Number.isFinite(retryAt) ? Math.max(0, Math.ceil((retryAt - Date.now()) / 1_000)) : undefined;
}

function toWorkApiError(error: AxiosError<unknown>): WorkApiError {
  const envelope = error.response ? parseSafely(error.response.data) : undefined;
  const status = error.response?.status;
  const retryAfter = retryAfterSeconds(error.response?.headers?.["retry-after"]);

  if (envelope && !isSuccessEnvelope(envelope)) {
    return new WorkApiError({
      message: envelope.message,
      status,
      businessCode: envelope.businessCode,
      traceId: envelope.traceId,
      fieldErrors: getFieldErrors(envelope),
      retryAfterSeconds: retryAfter,
    });
  }

  return new WorkApiError({
    message: error.message || "Unable to reach the Work service.",
    status,
    retryAfterSeconds: retryAfter,
  });
}

interface RetriableRequestConfig extends InternalAxiosRequestConfig {
  _workSessionRetried?: boolean;
}

function parseSafely(payload: unknown): ApiEnvelope<unknown> | undefined {
  try {
    return parseApiEnvelope(payload);
  } catch {
    return undefined;
  }
}

export const workApi = axios.create({
  baseURL: workApiBaseUrl,
  timeout: 15_000,
  // The Work API uses an Identity-issued Bearer token. The rotating refresh
  // cookie is sent only to Identity by session-client.ts.
  withCredentials: false,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

workApi.interceptors.request.use((config) => {
  const token = getAccessToken();
  const requestId = newRequestId();

  if (token) {
    config.headers.set("Authorization", `Bearer ${token}`);
  }

  if (requestId) {
    config.headers.set("X-Client-Request-Id", requestId);
  }

  return config;
});

workApi.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<unknown>) => {
    const config = error.config as RetriableRequestConfig | undefined;

    if (error.response?.status === 401 && config && !config._workSessionRetried) {
      config._workSessionRetried = true;
      const session = await restoreWorkSession();

      if (session) {
        useSessionStore.getState().setSession(session);
        config.headers.set("Authorization", `Bearer ${session.accessToken}`);
        return workApi.request(config);
      }

      clearSession();
    }

    return Promise.reject(toWorkApiError(error));
  },
);

export async function apiRequest<TData, TMeta extends ApiMeta = ApiMeta>(
  config: AxiosRequestConfig,
): Promise<ApiSuccessEnvelope<TData, TMeta>> {
  const response = await workApi.request<unknown>(config);
  const envelope = parseApiEnvelope<TData>(response.data);

  if (!isSuccessEnvelope(envelope)) {
    throw new WorkApiError({
      message: envelope.message,
      status: response.status,
      businessCode: envelope.businessCode,
      traceId: envelope.traceId,
      fieldErrors: getFieldErrors(envelope),
      retryAfterSeconds: retryAfterSeconds(response.headers["retry-after"]),
    });
  }

  return envelope as ApiSuccessEnvelope<TData, TMeta>;
}

export function isRetryableApiError(error: unknown): boolean {
  if (!(error instanceof WorkApiError)) {
    return true;
  }

  return error.status === undefined || error.status >= 500;
}

export function createIdempotencyKey(): string {
  return newRequestId() ?? `${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

export function mutationHeaders({
  idempotencyKey,
  version,
}: {
  idempotencyKey?: string;
  version?: number | string;
}): Record<string, string> {
  return {
    ...(idempotencyKey ? { "Idempotency-Key": idempotencyKey } : {}),
    ...(version !== undefined ? { "If-Match": `"${version}"` } : {}),
  };
}
