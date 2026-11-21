export interface GS05ReviewAuthorResponse {
  id: number;
  full_name: string;
  avatar_url: string | null;
}

export interface GS05ReviewReplyResponse {
  id: number;
  discussion_id: number;
  content: string;
  author: GS05ReviewAuthorResponse;
  created_at: string;
}

export interface GS05ReviewResponse {
  id: number;
  course_id: number;
  title: string | null;
  content: string;
  author: GS05ReviewAuthorResponse;
  status: string;
  created_at: string;
  comments: GS05ReviewReplyResponse[];
}

export interface GS05ReviewPagination {
  page: number;
  size: number;
  total: number;
  total_pages: number;
}

export interface GS05CourseReviewsPage {
  items: GS05ReviewResponse[];
  pagination: GS05ReviewPagination;
}

export interface GS05ReviewReply {
  authorName: string;
  content: string;
}

export interface GS05ReviewItem {
  authorName: string;
  content: string;
  replies: GS05ReviewReply[];
}

export type GS05ReviewsState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'empty' }
  | {
      status: 'ready';
      items: GS05ReviewItem[];
      page: number;
      totalPages: number;
      snapshotMismatch?: boolean;
    }
  | { status: 'out-of-range'; page: number }
  | { status: 'not-found' }
  | { status: 'error' };

export function toGS05ReviewItems(items: GS05ReviewResponse[]): GS05ReviewItem[] {
  return items.map((review) => ({
    authorName: review.author.full_name,
    content: review.content,
    replies: review.comments.map((reply) => ({
      authorName: reply.author.full_name,
      content: reply.content,
    })),
  }));
}

export function isGS05CourseReviewsPage(value: unknown): value is GS05CourseReviewsPage {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) {
    return false;
  }

  const items = value['items'];
  const pagination = value['pagination'];
  if (
    !isPositiveInteger(pagination['page']) ||
    !isPositiveInteger(pagination['size']) ||
    !isNonnegativeInteger(pagination['total']) ||
    !isNonnegativeInteger(pagination['total_pages'])
  ) {
    return false;
  }

  return (
    items.every(isGS05Review) &&
    pagination['size'] === 20 &&
    items.length <= pagination['size'] &&
    pagination['total_pages'] ===
      (pagination['total'] === 0 ? 0 : Math.ceil(pagination['total'] / pagination['size'])) &&
    (pagination['total'] > 0 || items.length === 0)
  );
}

function isGS05Review(value: unknown): value is GS05ReviewResponse {
  if (!isRecord(value) || !isRecord(value['author']) || !Array.isArray(value['comments'])) {
    return false;
  }

  const reviewId = value['id'];
  return (
    isPositiveInteger(reviewId) &&
    isPositiveInteger(value['course_id']) &&
    (value['title'] === null || typeof value['title'] === 'string') &&
    typeof value['content'] === 'string' &&
    isGS05Author(value['author']) &&
    value['status'] === 'ACTIVE' &&
    isNonemptyString(value['created_at']) &&
    value['comments'].every(
      (reply) => isGS05Reply(reply) && reply.discussion_id === reviewId,
    )
  );
}

function isGS05Reply(value: unknown): value is GS05ReviewReplyResponse {
  if (!isRecord(value) || !isRecord(value['author'])) return false;
  return (
    isPositiveInteger(value['id']) &&
    isPositiveInteger(value['discussion_id']) &&
    typeof value['content'] === 'string' &&
    isGS05Author(value['author']) &&
    isNonemptyString(value['created_at'])
  );
}

function isGS05Author(value: unknown): value is GS05ReviewAuthorResponse {
  if (!isRecord(value)) return false;
  return (
    isPositiveInteger(value['id']) &&
    typeof value['full_name'] === 'string' &&
    (value['avatar_url'] === null || typeof value['avatar_url'] === 'string')
  );
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isPositiveInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value > 0;
}

function isNonnegativeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value >= 0;
}

function isNonemptyString(value: unknown): value is string {
  return typeof value === 'string' && value.length > 0;
}
