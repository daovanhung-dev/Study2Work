export type SH07OperationStatus = 'QUEUED' | 'FAILED' | 'SENT';

export interface SH07NotificationOperation {
  readonly id: string;
  readonly kind: 'NOTIFICATION_DISPATCH';
  readonly status: SH07OperationStatus;
  readonly submitted_at: string;
  readonly updated_at: string;
  readonly completed_at?: string | null;
}

export function isOperationUuid(value: unknown): value is string {
  return typeof value === 'string' &&
    /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/.test(value);
}

export function parseSH07Operation(value: unknown, expectedId: string): SH07NotificationOperation | null {
  if (!isRecord(value) || !isOperationUuid(value['id']) || value['id'].toLowerCase() !== expectedId.toLowerCase()) {
    return null;
  }
  if (
    value['kind'] !== 'NOTIFICATION_DISPATCH' ||
    !isOperationStatus(value['status']) ||
    !isTimestamp(value['submitted_at']) ||
    !isTimestamp(value['updated_at']) ||
    (value['completed_at'] !== undefined && value['completed_at'] !== null && !isTimestamp(value['completed_at']))
  ) {
    return null;
  }
  return {
    id: value['id'],
    kind: 'NOTIFICATION_DISPATCH',
    status: value['status'],
    submitted_at: value['submitted_at'],
    updated_at: value['updated_at'],
    completed_at: typeof value['completed_at'] === 'string' ? value['completed_at'] : null,
  };
}

function isOperationStatus(value: unknown): value is SH07OperationStatus {
  return value === 'QUEUED' || value === 'FAILED' || value === 'SENT';
}

function isTimestamp(value: unknown): value is string {
  return typeof value === 'string' && value.trim().length > 0 && Number.isFinite(Date.parse(value));
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}
