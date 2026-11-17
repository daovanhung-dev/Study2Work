export type MentorApiId = number | string;

export interface MentorPage<T> {
  items: T[];
  pagination: { page: number; size: number; total: number; total_pages: number };
}

export interface MentorCourse {
  id: MentorApiId;
  title: string;
  description?: string | null;
  thumbnail_url?: string | null;
  price: string;
  status: string;
  mentor: { id: MentorApiId; full_name: string; avatar_url?: string | null };
}

export interface MentorUploadAsset {
  id: MentorApiId;
  name: string;
  url: string;
  content_type: string;
  size_bytes: number;
  status: string;
}

export interface MentorLecture {
  id: MentorApiId;
  course_id: MentorApiId;
  title: string;
  content: string | null;
  assets: MentorUploadAsset[];
  order: number;
  status: string;
}

export interface MentorContent {
  id: MentorApiId;
  course_id: MentorApiId;
  content_type: string;
  title: string;
  payload: Record<string, unknown>;
  status: string;
  parent_id?: MentorApiId | null;
  order: number;
}

export interface MentorSubmission {
  id: MentorApiId;
  assignment_id: MentorApiId;
  user_id: MentorApiId;
  content?: string | null;
  files: MentorUploadAsset[];
  status: string;
  submitted_at: string;
  score?: string | null;
  feedback?: string | null;
}

export interface MentorSupportRequest {
  id: MentorApiId;
  course_id: MentorApiId;
  student: { id: MentorApiId; full_name: string; avatar_url?: string | null };
  status: string;
  messages: Array<{
    id: MentorApiId;
    author: { id: MentorApiId; full_name: string; avatar_url?: string | null };
    content: string;
    attachments: MentorUploadAsset[];
    created_at: string;
  }>;
  created_at: string;
  resolved_at?: string | null;
}

export interface MentorStudentSummary {
  id: MentorApiId;
  full_name: string;
  avatar_url?: string | null;
}

export interface MentorCourseProgressRow {
  student: MentorStudentSummary;
  completed_lessons: number;
  total_lessons: number;
  progress_percent: number;
}

export interface MentorStudentProgress {
  course_id: MentorApiId;
  student: MentorStudentSummary;
  summary: { completed_lessons: number; total_lessons: number; progress_percent: number };
  lessons: Array<{
    lesson_id: MentorApiId;
    title: string;
    order: number;
    progress_status: 'NOT_STARTED' | 'IN_PROGRESS' | 'COMPLETED';
    progress_percent: number;
    last_accessed_at: string | null;
    completed_at: string | null;
  }>;
}

export interface MentorCourseAnalytics {
  tracked_lesson_accesses: number;
  students_with_activity: number;
  last_activity_at: string | null;
}

export interface MentorNotificationOperation {
  id: string;
  kind: string;
  status: string;
  owner_id: MentorApiId;
  submitted_at: string;
  updated_at: string;
  completed_at?: string | null;
}

export function toSafeMentorId(value: unknown): string | null {
  if (typeof value === 'string') {
    if (!/^[1-9]\d*$/.test(value)) return null;
    try {
      return BigInt(value) <= 9_223_372_036_854_775_807n ? value : null;
    } catch {
      return null;
    }
  }
  if (typeof value === 'number' && Number.isSafeInteger(value) && value > 0) {
    return String(value);
  }
  return null;
}

export function isSafeMentorPathId(value: string | null | undefined): value is string {
  return toSafeMentorId(value) === value;
}
