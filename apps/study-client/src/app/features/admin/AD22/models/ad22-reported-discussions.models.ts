import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminDiscussion, AdminPage } from '../../admin-api.models';

const PAGE_SIZE = 20;

export function isAD22ReportedDiscussionsEnvelope(
  value: unknown,
  requestedPage: number,
): value is ApiEnvelope<AdminPage<AdminDiscussion>> {
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

  const page = value['data'];
  if (!isRecord(page) || !Array.isArray(page['items']) || !isRecord(page['pagination'])) {
    return false;
  }

  const pagination = page['pagination'];
  const pageNumber = pagination['page'];
  const size = pagination['size'];
  const total = pagination['total'];
  const totalPages = pagination['total_pages'];
  if (
    !isPositiveInt32(pageNumber) ||
    pageNumber !== requestedPage ||
    size !== PAGE_SIZE ||
    !isNonnegativeSafeInteger(total) ||
    !isNonnegativeInt32(totalPages) ||
    totalPages !== (total === 0 ? 0 : Math.ceil(total / PAGE_SIZE)) ||
    page['items'].length > PAGE_SIZE
  ) {
    return false;
  }

  const seenIds = new Set<number>();
  return page['items'].every((item) => {
    if (!isAD22Discussion(item)) return false;
    if (seenIds.has(item.id)) return false;
    seenIds.add(item.id);
    return true;
  });
}

function isAD22Discussion(value: unknown): value is AdminDiscussion {
  if (!isRecord(value) || !isRecord(value['author']) || !Array.isArray(value['comments'])) {
    return false;
  }

  const discussionId = value['id'];
  return (
    isPositiveInteger(discussionId) &&
    isPositiveInteger(value['course_id']) &&
    typeof value['title'] === 'string' &&
    typeof value['content'] === 'string' &&
    isAD22Author(value['author']) &&
    typeof value['status'] === 'string' &&
    value['comments'].every(
      (comment) =>
        isAD22Comment(comment) && comment.discussion_id === discussionId,
    )
  );
}

function isAD22Comment(value: unknown): value is AdminDiscussion['comments'][number] {
  return (
    isRecord(value) &&
    isPositiveInteger(value['id']) &&
    isPositiveInteger(value['discussion_id']) &&
    typeof value['content'] === 'string' &&
    isRecord(value['author']) &&
    isAD22Author(value['author']) &&
    isDateString(value['created_at'])
  );
}

function isAD22Author(value: unknown): value is AdminDiscussion['author'] {
  return (
    isRecord(value) &&
    isPositiveInteger(value['id']) &&
    typeof value['full_name'] === 'string' &&
    (value['avatar_url'] === undefined ||
      value['avatar_url'] === null ||
      typeof value['avatar_url'] === 'string')
  );
}

function isDateString(value: unknown): value is string {
  return typeof value === 'string' && value.length > 0 && Number.isFinite(Date.parse(value));
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isPositiveInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value > 0;
}

function isPositiveInt32(value: unknown): value is number {
  return (
    typeof value === 'number' &&
    Number.isInteger(value) &&
    value > 0 &&
    value <= 2_147_483_647
  );
}

function isNonnegativeInt32(value: unknown): value is number {
  return (
    typeof value === 'number' &&
    Number.isInteger(value) &&
    value >= 0 &&
    value <= 2_147_483_647
  );
}

function isNonnegativeSafeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isSafeInteger(value) && value >= 0;
}
