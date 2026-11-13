export interface MentorCourseActivityAnalyticsDto {
  readonly tracked_lesson_accesses: number;
  readonly students_with_activity: number;
  readonly last_activity_at: string | null;
}

export function parseCourseIdParam(raw: string | null | undefined): number | null {
  if (!raw) {
    return null;
  }
  const trimmed = raw.trim();
  if (!/^[1-9]\d*$/.test(trimmed)) {
    return null;
  }
  const parsed = Number(trimmed);
  return Number.isSafeInteger(parsed) && parsed > 0 ? parsed : null;
}
