import type { StudentEnrollment } from './student-enrollment.models';
import { toSafeStudyId } from './student-api.models';

export function isStudentEnrollment(value: unknown): value is StudentEnrollment {
  if (typeof value !== 'object' || value === null) return false;
  const enrollment = value as Record<string, unknown>;
  return (
    toSafeStudyId(enrollment['id']) !== null &&
    toSafeStudyId(enrollment['course_id']) !== null &&
    toSafeStudyId(enrollment['user_id']) !== null &&
    typeof enrollment['status'] === 'string' &&
    isDateString(enrollment['enrolled_at']) &&
    (enrollment['completed_at'] === undefined ||
      enrollment['completed_at'] === null ||
      isDateString(enrollment['completed_at']))
  );
}

function isDateString(value: unknown): value is string {
  return typeof value === 'string' && Number.isFinite(Date.parse(value));
}
