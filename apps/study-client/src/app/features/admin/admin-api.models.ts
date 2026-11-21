export interface AdminUserProfile {
  readonly id: number;
  readonly full_name: string;
  readonly email: string;
  readonly role: string;
  readonly avatar_url: string | null;
  readonly phone: string | null;
  readonly status: string;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface AdminPagination {
  readonly page: number;
  readonly size: number;
  readonly total: number;
  readonly total_pages: number;
}

export interface AdminPage<T> {
  readonly items: readonly T[];
  readonly pagination: AdminPagination;
}

export interface AdminMentorSummary {
  readonly id: number;
  readonly full_name: string;
  readonly avatar_url: string | null;
}

export interface AdminCourse {
  readonly id: number;
  readonly title: string;
  readonly description: string | null;
  readonly thumbnail_url: string | null;
  readonly price: string;
  readonly status: string;
  readonly mentor: AdminMentorSummary;
}

export interface AdminContent {
  readonly id: number;
  readonly course_id: number;
  readonly content_type: string;
  readonly title: string;
  readonly payload: Readonly<Record<string, unknown>>;
  readonly status: string;
  readonly parent_id?: number | null;
  readonly order: number;
}

export interface AdminLesson {
  readonly id: number;
  readonly course_id: number;
  readonly title: string;
  readonly content: string | null;
  readonly video_url: string | null;
  readonly order: number;
  readonly status: string;
}

export interface AdminQuiz {
  readonly id: number;
  readonly course_id: number;
  readonly title: string;
  readonly duration_minutes?: number | null;
  readonly passing_score: string;
  readonly questions: readonly Readonly<Record<string, unknown>>[];
}

export interface AdminQuizStatistics {
  readonly quiz_id: number;
  readonly attempt_count: number;
  readonly submitted_attempt_count: number;
  readonly graded_attempt_count: number;
  readonly average_score: string | null;
  readonly passed_attempt_count: number | null;
  readonly pass_rate_percent: string | null;
}

export type AdminNotificationChannel = 'EMAIL' | 'PUSH';
export type AdminNotificationStatus = 'FAILED' | 'QUEUED' | 'SENT';

export interface AdminNotification {
  readonly id: number;
  readonly title: string;
  readonly content: string;
  readonly channels: readonly AdminNotificationChannel[];
  readonly status: AdminNotificationStatus;
  readonly created_at: string;
}

export interface AdminDiscussionAuthor {
  readonly id: number;
  readonly full_name: string;
  readonly avatar_url?: string | null;
}

export interface AdminDiscussionComment {
  readonly id: number;
  readonly discussion_id: number;
  readonly content: string;
  readonly author: AdminDiscussionAuthor;
  readonly created_at: string;
}

export interface AdminDiscussion {
  readonly id: number;
  readonly course_id: number;
  readonly title: string;
  readonly content: string;
  readonly author: AdminDiscussionAuthor;
  readonly status: string;
  readonly comments: readonly AdminDiscussionComment[];
}
