import type { StudentAchievement, StudentPage } from './student-api.models';

export function isStudentAchievementPage(
  value: unknown,
): value is StudentPage<StudentAchievement> {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) {
    return false;
  }

  const pagination = value['pagination'];
  const total = pagination['total'];
  if (
    pagination['page'] !== 1 ||
    pagination['size'] !== Math.max(value['items'].length, 1) ||
    !isNonnegativeSafeInteger(total) ||
    pagination['total_pages'] !== (total > 0 ? 1 : 0)
  ) {
    return false;
  }

  const seenIds = new Set<number>();
  let previousAwardedAt = Number.POSITIVE_INFINITY;
  let previousId = Number.POSITIVE_INFINITY;
  return value['items'].every((item: unknown) => {
    if (
      !isRecord(item) ||
      !isPositiveSafeInteger(item['id']) ||
      typeof item['code'] !== 'string' ||
      typeof item['title'] !== 'string' ||
      typeof item['awarded_at'] !== 'string' ||
      (item['course_id'] !== null &&
        item['course_id'] !== undefined &&
        !isPositiveSafeInteger(item['course_id']))
    ) {
      return false;
    }

    const awardedAt = Date.parse(item['awarded_at']);
    const id = item['id'];
    if (
      !Number.isFinite(awardedAt) ||
      awardedAt > previousAwardedAt ||
      (awardedAt === previousAwardedAt && id >= previousId) ||
      seenIds.has(id)
    ) {
      return false;
    }
    seenIds.add(id);
    previousAwardedAt = awardedAt;
    previousId = id;
    return true;
  });
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

function isPositiveSafeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isSafeInteger(value) && value > 0;
}

function isNonnegativeSafeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isSafeInteger(value) && value >= 0;
}
