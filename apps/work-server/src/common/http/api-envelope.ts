export interface ApiSuccessEnvelope<TData = unknown, TMeta extends ApiMeta = ApiMeta> {
  success: true;
  businessCode: string;
  message: string;
  data: TData;
  meta: TMeta;
  traceId: string;
}

export interface ApiErrorDetail {
  field?: string;
  code: string;
  message: string;
}

export type ApiMeta = Record<string, unknown> & {
  fieldErrors?: ApiErrorDetail[];
};

export type ApiErrorMeta = ApiMeta & {
  fieldErrors: ApiErrorDetail[];
};

export interface ApiErrorEnvelope {
  success: false;
  businessCode: string;
  message: string;
  data: null;
  meta: ApiErrorMeta;
  traceId: string;
}

export type ApiEnvelope<TData = unknown, TMeta extends ApiMeta = ApiMeta> =
  | ApiSuccessEnvelope<TData, TMeta>
  | ApiErrorEnvelope;

export function isApiEnvelope(value: unknown): value is ApiEnvelope {
  if (!value || typeof value !== "object" || !("success" in value)) {
    return false;
  }

  return typeof value.success === "boolean";
}
