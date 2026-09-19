export interface UseCaseResult<T = unknown> {
  statusCode: number;
  businessCode: string;
  message: string;
  data?: T;
  meta?: Record<string, unknown>;
}
