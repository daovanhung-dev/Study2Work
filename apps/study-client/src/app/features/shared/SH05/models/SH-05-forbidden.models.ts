export interface AccessFailureViewModel {
  readonly status: 401 | 403 | null;
  readonly title: string;
  readonly description: string;
  readonly traceId: string | null;
}
