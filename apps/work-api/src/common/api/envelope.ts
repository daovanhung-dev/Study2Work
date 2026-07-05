export interface ApiHandlerResult<TData = unknown> {
  businessCode: string;
  message: string;
  data: TData;
  meta?: Record<string, unknown>;
}

export interface ApiSuccessEnvelope<TData = unknown> {
  success: true;
  businessCode: string;
  message: string;
  data: TData;
  meta: Record<string, unknown>;
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

export function createSuccessEnvelope<TData>(
  result: ApiHandlerResult<TData>,
  traceId: string,
): ApiSuccessEnvelope<TData> {
  return {
    success: true,
    businessCode: result.businessCode,
    message: result.message,
    data: result.data,
    meta: result.meta ?? {},
    traceId,
  };
}

export function createErrorEnvelope(args: {
  businessCode: string;
  message: string;
  errors?: ApiErrorDetail[];
  traceId: string;
}): ApiErrorEnvelope {
  return {
    success: false,
    businessCode: args.businessCode,
    message: args.message,
    errors: args.errors ?? [],
    traceId: args.traceId,
  };
}
