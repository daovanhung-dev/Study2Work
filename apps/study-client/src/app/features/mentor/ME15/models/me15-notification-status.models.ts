export type NotificationDeliveryState = 'QUEUED' | 'SENT' | 'FAILED';

export interface NotificationStatusOperationDto {
  readonly operation_id: string;
  readonly status: NotificationDeliveryState;
}

export interface NotificationStatusItemVm {
  readonly notificationId: number;
  readonly operationId: string;
  readonly status: NotificationDeliveryState;
}

export interface NotificationStatusSummaryVm {
  readonly total: number;
  readonly queued: number;
  readonly sent: number;
  readonly failed: number;
}

export function parsePositiveInt(raw: string | number | null | undefined): number | null {
  if (raw === null || raw === undefined) {
    return null;
  }
  const str = String(raw).trim();
  if (!/^[1-9]\d*$/.test(str)) {
    return null;
  }
  const num = Number(str);
  return Number.isSafeInteger(num) && num > 0 ? num : null;
}

export function parseNotificationIds(
  routeId: string | null | undefined,
  queryIds: string | null | undefined,
): number[] {
  const seen = new Set<number>();
  const single = parsePositiveInt(routeId);
  if (single) {
    seen.add(single);
  }
  if (queryIds) {
    for (const part of queryIds.split(',')) {
      const parsed = parsePositiveInt(part);
      if (parsed) {
        seen.add(parsed);
      }
    }
  }
  return Array.from(seen);
}

export function computeNotificationSummary(
  items: readonly NotificationStatusItemVm[],
): NotificationStatusSummaryVm {
  let queued = 0;
  let sent = 0;
  let failed = 0;
  for (const item of items) {
    if (item.status === 'SENT') {
      sent += 1;
    } else if (item.status === 'FAILED') {
      failed += 1;
    } else {
      queued += 1;
    }
  }
  return {
    total: items.length,
    queued,
    sent,
    failed,
  };
}
