export type LessonProgressStatus = 'NOT_STARTED' | 'IN_PROGRESS' | 'COMPLETED';

export interface Me17StudentSummaryDto {
  readonly id: number;
  readonly full_name: string;
  readonly avatar_url?: string | null;
}

export interface StudentLessonProgressDto {
  readonly lesson_id: number;
  readonly title: string;
  readonly order: number;
  readonly progress_status: LessonProgressStatus;
  readonly progress_percent: number;
  readonly last_accessed_at?: string | null;
  readonly completed_at?: string | null;
}

export interface StudentCourseProgressSummaryDto {
  readonly completed_lessons: number;
  readonly total_lessons: number;
  readonly progress_percent: number;
}

export interface StudentCourseProgressDto {
  readonly course_id: number;
  readonly student: Me17StudentSummaryDto;
  readonly summary: StudentCourseProgressSummaryDto;
  readonly lessons: readonly StudentLessonProgressDto[];
}

const MAX_INT64 = 9223372036854775807n;

export function parsePositiveInt64(raw: string | null | undefined): number | null {
  if (!raw) {
    return null;
  }
  const trimmed = raw.trim();
  if (!/^[1-9]\d*$/.test(trimmed)) {
    return null;
  }
  try {
    const big = BigInt(trimmed);
    if (big < 1n || big > MAX_INT64) {
      return null;
    }
    return Number(big);
  } catch {
    return null;
  }
}

export function formatLessonProgressStatus(status: LessonProgressStatus): string {
  switch (status) {
    case 'COMPLETED':
      return 'Đã hoàn thành (COMPLETED)';
    case 'IN_PROGRESS':
      return 'Đang học (IN_PROGRESS)';
    case 'NOT_STARTED':
      return 'Chưa bắt đầu (NOT_STARTED)';
  }
}
