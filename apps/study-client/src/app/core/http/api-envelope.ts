export interface ApiEnvelope<T> {
  success: boolean;
  businessCode: string;
  message: string;
  data: T;
  meta: Record<string, unknown>;
  traceId: string;
}
