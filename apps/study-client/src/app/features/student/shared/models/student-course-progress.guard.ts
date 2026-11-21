import type { StudentCourseProgress } from './student-api.models';
import { toSafeStudyId } from './student-api.models';

export function isStudentCourseProgress(
  value: unknown,
  courseId: string,
): value is StudentCourseProgress {
  if (typeof value !== 'object' || value === null) return false;
  const progress = value as Record<string, unknown>;
  const completed = progress['completed_lessons'];
  const total = progress['total_lessons'];
  return (
    typeof progress['course_id'] === 'number' &&
    toSafeStudyId(progress['course_id']) === courseId &&
    isNonnegativeSafeInteger(completed) &&
    isNonnegativeSafeInteger(total) &&
    completed <= total &&
    progress['progress_percent'] === (total > 0 ? Math.floor((completed * 100) / total) : 0) &&
    progress['has_content'] === (total > 0)
  );
}

function isNonnegativeSafeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isSafeInteger(value) && value >= 0;
}
