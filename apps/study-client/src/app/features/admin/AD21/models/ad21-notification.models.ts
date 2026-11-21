import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminNotification } from '../../admin-api.models';

const MAX_INT64 = 9_223_372_036_854_775_807n;
const NOTIFICATION_STATUSES = new Set(['FAILED', 'QUEUED', 'SENT']);
const NOTIFICATION_CHANNELS = new Set(['EMAIL', 'PUSH']);

export function isAD21NotificationEnvelope(
  value: unknown,
  requestedId: string,
): value is ApiEnvelope<AdminNotification> {
  if (
    !isRecord(value) ||
    value['success'] !== true ||
    value['businessCode'] !== 'DESIGN_RESOURCE_RETRIEVED' ||
    typeof value['message'] !== 'string' ||
    !isRecord(value['meta']) ||
    typeof value['traceId'] !== 'string'
  ) {
    return false;
  }

  const expectedId = parsePositiveInt64(requestedId);
  return expectedId !== null && isAD21Notification(value['data'], expectedId);
}

function isAD21Notification(value: unknown, expectedId: bigint): value is AdminNotification {
  if (!isRecord(value)) return false;
  const id = value['id'];
  const channels = value['channels'];
  const status = value['status'];
  const createdAt = value['created_at'];
  if (
    typeof id !== 'number' ||
    !Number.isSafeInteger(id) ||
    id <= 0 ||
    BigInt(id) !== expectedId ||
    typeof value['title'] !== 'string' ||
    typeof value['content'] !== 'string' ||
    !Array.isArray(channels) ||
    channels.length === 0 ||
    !channels.every(
      (channel) => typeof channel === 'string' && NOTIFICATION_CHANNELS.has(channel),
    ) ||
    new Set(channels).size !== channels.length ||
    typeof status !== 'string' ||
    !NOTIFICATION_STATUSES.has(status) ||
    typeof createdAt !== 'string' ||
    createdAt.length === 0 ||
    !Number.isFinite(Date.parse(createdAt))
  ) {
    return false;
  }

  return true;
}

function parsePositiveInt64(value: string): bigint | null {
  if (!/^\d+$/.test(value) || value.length > 19) return null;
  try {
    const parsed = BigInt(value);
    return parsed > 0n && parsed <= MAX_INT64 ? parsed : null;
  } catch {
    return null;
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}
