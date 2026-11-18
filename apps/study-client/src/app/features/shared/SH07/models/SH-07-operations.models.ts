export interface OperationDto {
  readonly id: string;
  readonly kind: 'NOTIFICATION_DISPATCH';
  readonly status: 'QUEUED' | 'FAILED' | 'SENT';
  readonly owner_id: number;
  readonly submitted_at: string;
  readonly updated_at: string;
  readonly completed_at?: string;
  readonly result?: Record<string, unknown>;
}

export interface SystemOperationsState {
  readonly kind: 'missing-context' | 'loading' | 'ready' | 'not-found' | 'unavailable' | 'error';
  readonly title: string;
  readonly message: string;
  readonly referenceId: string | null;
  readonly operation?: OperationDto;
  readonly traceId?: string | null;
}
