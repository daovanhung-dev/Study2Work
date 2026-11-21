import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminDiscussion, AdminPage } from '../../admin-api.models';

const MAX_INT64 = 9_223_372_036_854_775_807n;

export function isPositiveSignedInt64DiscussionId(value: string): boolean {
  return parsePositiveInt64(value) !== null;
}

export function isAD23DiscussionEnvelope(
  value: unknown,
  requestedId: string,
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

  const expectedId = parsePositiveInt64(requestedId);
  const page = value['data'];
  if (
    expectedId === null ||
    !isRecord(page) ||
    !Array.isArray(page['items']) ||
    page['items'].length !== 1 ||
    !isRecord(page['pagination']) ||
    page['pagination']['page'] !== 1 ||
    page['pagination']['size'] !== 1 ||
    page['pagination']['total'] !== 1 ||
    page['pagination']['total_pages'] !== 1
  ) {
    return false;
  }

  const discussion = page['items'][0];
  return isAD23Discussion(discussion, expectedId);
}

function isAD23Discussion(value: unknown, expectedId: bigint): value is AdminDiscussion {
  if (!isRecord(value) || !isRecord(value['author']) || !Array.isArray(value['comments'])) {
    return false;
  }

  const discussionId = value['id'];
  if (
    typeof discussionId !== 'number' ||
    !Number.isSafeInteger(discussionId) ||
    discussionId <= 0 ||
    BigInt(discussionId) !== expectedId ||
    !isPositiveInteger(value['course_id']) ||
    typeof value['title'] !== 'string' ||
    typeof value['content'] !== 'string' ||
    !isAD23Author(value['author']) ||
    typeof value['status'] !== 'string'
  ) {
    return false;
  }

  return value['comments'].every(
    (comment) => isAD23Comment(comment, discussionId),
  );
}

function isAD23Comment(value: unknown, parentId: number): boolean {
  if (!isRecord(value)) return false;
  const discussionId = value['discussion_id'];
  return (
    isPositiveInteger(value['id']) &&
    typeof discussionId === 'number' &&
    Number.isSafeInteger(discussionId) &&
    discussionId === parentId &&
    typeof value['content'] === 'string' &&
    isAD23Author(value['author']) &&
    isDateString(value['created_at'])
  );
}

function isAD23Author(value: unknown): boolean {
  return (
    isRecord(value) &&
    isPositiveInteger(value['id']) &&
    typeof value['full_name'] === 'string' &&
    (value['avatar_url'] === undefined ||
      value['avatar_url'] === null ||
      typeof value['avatar_url'] === 'string')
  );
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

function isDateString(value: unknown): value is string {
  return typeof value === 'string' && value.length > 0 && Number.isFinite(Date.parse(value));
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isPositiveInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value > 0;
}
