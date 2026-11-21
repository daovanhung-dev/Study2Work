import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminNotification, AdminPage } from '../../admin-api.models';

const PAGE_SIZE = 20;
const NOTIFICATION_STATUSES = new Set(['FAILED', 'QUEUED', 'SENT']);
const NOTIFICATION_CHANNELS = new Set(['EMAIL', 'PUSH']);

export function isAD19NotificationsEnvelope(
  value: unknown,
  query: { status?: string; channel?: string; page?: number },
): value is ApiEnvelope<AdminPage<AdminNotification>> {
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

  const requestedPage = query.page ?? 1;
  return isAD19NotificationsPage(value['data'], requestedPage, query);
}

export function hasAD19NotificationsPageCountMismatch(
  page: AdminPage<AdminNotification>,
): boolean {
  const { page: pageNumber, size, total } = page.pagination;
  if (!Number.isSafeInteger(total)) return true;

  const offset = (pageNumber - 1) * size;
  const expectedItems = Math.min(size, Math.max(total - offset, 0));
  return page.items.length !== expectedItems;
}

function isAD19NotificationsPage(
  value: unknown,
  requestedPage: number,
  query: { status?: string; channel?: string },
): value is AdminPage<AdminNotification> {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) {
    return false;
  }

  const pagination = value['pagination'];
  const page = pagination['page'];
  const size = pagination['size'];
  const total = pagination['total'];
  const totalPages = pagination['total_pages'];
  if (
    !isPositiveInt32(page) ||
    page !== requestedPage ||
    size !== PAGE_SIZE ||
    !isNonnegativeInteger(total) ||
    !isNonnegativeInt32(totalPages) ||
    (Number.isSafeInteger(total) &&
      totalPages !== (total === 0 ? 0 : Math.ceil(total / PAGE_SIZE)))
  ) {
    return false;
  }

  const items = value['items'];
  if (items.length > PAGE_SIZE) {
    return false;
  }

  const seenIds = new Set<number>();
  return items.every((item) => {
    if (!isRecord(item)) return false;
    const id = item['id'];
    const channels = item['channels'];
    const status = item['status'];
    const createdAt = item['created_at'];
    if (
      !isPositiveInteger(id) ||
      (Number.isSafeInteger(id) && seenIds.has(id)) ||
      typeof item['title'] !== 'string' ||
      typeof item['content'] !== 'string' ||
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
      !Number.isFinite(Date.parse(createdAt)) ||
      (query.status && status !== query.status) ||
      (query.channel && !channels.includes(query.channel))
    ) {
      return false;
    }

    if (Number.isSafeInteger(id)) seenIds.add(id);
    return true;
  });
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isPositiveInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value > 0;
}

function isPositiveInt32(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value > 0 && value <= 2_147_483_647;
}

function isNonnegativeInt32(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value >= 0 && value <= 2_147_483_647;
}

function isNonnegativeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value >= 0;
}
