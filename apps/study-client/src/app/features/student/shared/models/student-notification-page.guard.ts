import type { StudentNotification, StudentPage } from './student-api.models';
import { toSafeStudyId } from './student-api.models';

export const STUDENT_NOTIFICATION_PAGE_SIZE = 20;

export function isStudentNotificationPage(
  value: unknown,
  expectedPage: number,
  expectedSize = STUDENT_NOTIFICATION_PAGE_SIZE,
  unreadOnly = false,
): value is StudentPage<StudentNotification> {
  if (typeof value !== 'object' || value === null) return false;
  const page = value as Record<string, unknown>;
  const pagination = page['pagination'];
  if (
    !Array.isArray(page['items']) ||
    typeof pagination !== 'object' ||
    pagination === null
  ) {
    return false;
  }

  const meta = pagination as Record<string, unknown>;
  const total = meta['total'];
  return (
    page['items'].every(
      (item) => isStudentNotification(item) && (!unreadOnly || !item.is_read),
    ) &&
    page['items'].length <= expectedSize &&
    meta['page'] === expectedPage &&
    meta['size'] === expectedSize &&
    Number.isSafeInteger(total) &&
    Number(total) >= page['items'].length &&
    meta['total_pages'] === (Number(total) > 0 ? Math.ceil(Number(total) / expectedSize) : 0)
  );
}

export function isStudentNotification(value: unknown): value is StudentNotification {
  if (typeof value !== 'object' || value === null) return false;
  const item = value as Record<string, unknown>;
  return (
    toSafeStudyId(item['id']) !== null &&
    typeof item['title'] === 'string' &&
    typeof item['content'] === 'string' &&
    (item['type'] === undefined || item['type'] === null || typeof item['type'] === 'string') &&
    typeof item['is_read'] === 'boolean' &&
    (item['read_at'] === undefined ||
      item['read_at'] === null ||
      isDateString(item['read_at'])) &&
    isDateString(item['created_at'])
  );
}

export function isStudentReadNotificationPage(
  value: unknown,
  notificationId: string,
): boolean {
  if (!isStudentNotificationPage(value, 1, 1)) return false;
  const page = value as StudentPage<StudentNotification>;
  return (
    page.items.length === 1 &&
    toSafeStudyId(page.items[0].id) === notificationId &&
    page.items[0].is_read &&
    page.pagination.size === 1 &&
    page.pagination.total === 1 &&
    page.pagination.total_pages === 1
  );
}

export function isStudentNotificationReadSummary(value: unknown): value is { updated_count: number } {
  if (typeof value !== 'object' || value === null) return false;
  const summary = value as Record<string, unknown>;
  return Number.isSafeInteger(summary['updated_count']) && Number(summary['updated_count']) >= 0;
}

function isDateString(value: unknown): value is string {
  return typeof value === 'string' && Number.isFinite(Date.parse(value));
}
