import type { StudentProfile } from './student-api.models';
import { toSafeStudyId } from './student-api.models';

export function isStudentProfile(value: unknown): value is StudentProfile {
  if (typeof value !== 'object' || value === null) return false;
  const profile = value as Record<string, unknown>;
  return (
    toSafeStudyId(profile['id']) !== null &&
    typeof profile['full_name'] === 'string' &&
    typeof profile['email'] === 'string' &&
    typeof profile['role'] === 'string' &&
    (profile['avatar_url'] === null || typeof profile['avatar_url'] === 'string') &&
    (profile['phone'] === null || typeof profile['phone'] === 'string') &&
    typeof profile['status'] === 'string' &&
    typeof profile['created_at'] === 'string' &&
    Number.isFinite(Date.parse(profile['created_at'])) &&
    typeof profile['updated_at'] === 'string' &&
    Number.isFinite(Date.parse(profile['updated_at']))
  );
}

export function isSafeHttpUrl(value: unknown): value is string {
  if (typeof value !== 'string') return false;
  try {
    const parsed = new URL(value);
    return parsed.protocol === 'http:' || parsed.protocol === 'https:';
  } catch {
    return false;
  }
}
