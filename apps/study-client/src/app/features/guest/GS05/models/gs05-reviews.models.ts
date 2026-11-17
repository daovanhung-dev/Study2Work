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
  | { status: 'ready'; items: GS05ReviewItem[]; page: number; totalPages: number }
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
