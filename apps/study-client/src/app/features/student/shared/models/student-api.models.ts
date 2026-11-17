export type StudyId = string;

export interface StudentAuthor {
  id: number;
  full_name: string;
  avatar_url: string | null;
}

export interface StudentLesson {
  id: number;
  course_id: number;
  title: string;
  content?: string | null;
  video_url?: string | null;
  order: number;
  status: string;
}

export interface StudentResource {
  id: number;
  name: string;
  type: string;
  url?: string | null;
  lesson_id?: number | null;
}

export interface StudentLessonResources extends StudentLesson {
  resources: StudentResource[];
}

export interface StudentCourseSummary {
  course_id: number;
  name: string;
  description?: string | null;
  thumbnail_url?: string | null;
  course_status?: string | null;
  enrollment_status: string;
  enrolled_at: string;
}

export interface StudentUploadAsset {
  id: number;
  name: string;
  url: string;
  content_type: string;
  size_bytes: number;
  status: string;
}

export interface StudentQuizChoice {
  id: number;
  choice_text: string;
}

export interface StudentQuizQuestion {
  id: number;
  text: string;
  type: string;
  choices: StudentQuizChoice[];
}

export interface StudentQuiz {
  id: number;
  course_id: number;
  title: string;
  duration_minutes?: number | null;
  passing_score: string;
  questions: StudentQuizQuestion[];
}

export interface StudentQuizAttempt {
  id: number;
  quiz_id: number;
  status: string;
  started_at: string;
  submitted_at?: string | null;
  score?: string | null;
  passed?: boolean | null;
  answers: StudentQuizAnswer[];
}

export interface StudentQuizAnswer {
  question_id: number;
  choice_ids?: number[] | null;
  text_answer?: string | null;
  correct?: boolean | null;
  score?: number | string | null;
}

export interface StudentAssignment {
  id: number;
  course_id: number;
  title: string;
  description?: string | null;
  due_at?: string | null;
  max_score: number | string;
}

export interface StudentSubmissionFile {
  id: number;
  name: string;
  url: string;
  content_type: string;
  size_bytes: number;
  status: string;
}

export interface StudentSubmission {
  id: number;
  assignment_id: number;
  user_id: number;
  content?: string | null;
  files: StudentSubmissionFile[];
  status: string;
  submitted_at: string;
  score?: number | string | null;
  feedback?: string | null;
}

export interface StudentCourseProgress {
  course_id: number;
  completed_lessons: number;
  total_lessons: number;
  progress_percent: number;
  has_content: boolean;
}

export interface StudentAchievement {
  id: number;
  code: string;
  title: string;
  awarded_at: string;
  course_id?: number | null;
}

export interface StudentPagination {
  page: number;
  size: number;
  total: number;
  total_pages: number;
}

export interface StudentPage<T> {
  items: T[];
  pagination: StudentPagination;
}

export interface StudentDiscussionComment {
  id: number;
  discussion_id: number;
  content: string;
  author: StudentAuthor;
  created_at: string;
}

export interface StudentDiscussion {
  id: number;
  course_id: number;
  title: string;
  content: string;
  author: StudentAuthor;
  status: string;
  comments: StudentDiscussionComment[];
}

export interface StudentNotification {
  id: number;
  title: string;
  content: string;
  type?: string | null;
  is_read: boolean;
  read_at?: string | null;
  created_at: string;
}

export function toSafeStudyId(value: unknown): StudyId | null {
  if (typeof value === 'number')
    return Number.isSafeInteger(value) && value > 0 ? String(value) : null;
  if (typeof value !== 'string' || !/^[1-9]\d*$/.test(value)) return null;
  try {
    const parsed = BigInt(value);
    return parsed <= 9_223_372_036_854_775_807n ? value : null;
  } catch {
    return null;
  }
}

export function toSafeStudyNumber(value: unknown): number | null {
  if (typeof value === 'number') return Number.isSafeInteger(value) && value > 0 ? value : null;
  if (typeof value !== 'string' || !/^[1-9]\d*$/.test(value)) return null;
  const parsed = Number(value);
  return Number.isSafeInteger(parsed) ? parsed : null;
}
