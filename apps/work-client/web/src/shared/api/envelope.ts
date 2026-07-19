export interface ApiSuccessEnvelope<TData, TMeta = Record<string, unknown>> {
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

export interface ApiErrorEnvelope {
  success: false;
  businessCode: string;
  message: string;
  errors: ApiErrorDetail[];
  traceId: string;
}

export type ApiEnvelope<TData, TMeta = Record<string, unknown>> =
  | ApiSuccessEnvelope<TData, TMeta>
  | ApiErrorEnvelope;

export function isSuccessEnvelope<TData>(
  envelope: ApiEnvelope<TData>,
): envelope is ApiSuccessEnvelope<TData> {
  return envelope.success;
}
